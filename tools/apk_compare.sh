#!/usr/bin/env bash

set -u

usage() {
    echo "Usage:"
    echo "  $0 NEW.apk"
    echo "  $0 OLD.apk NEW.apk"
    exit 2
}

if [ "$#" -eq 1 ]; then
    OLD_APK=""
    NEW_APK="$1"
elif [ "$#" -eq 2 ]; then
    OLD_APK="$1"
    NEW_APK="$2"
else
    usage
fi

if [ ! -f "$NEW_APK" ]; then
    echo "ERROR: New APK not found: $NEW_APK"
    exit 1
fi

if [ -n "$OLD_APK" ] && [ ! -f "$OLD_APK" ]; then
    echo "ERROR: Old APK not found: $OLD_APK"
    exit 1
fi

if command -v apkanalyzer >/dev/null 2>&1; then
    APKANALYZER="$(command -v apkanalyzer)"
elif [ -n "${ANDROID_HOME:-}" ] &&
     [ -x "$ANDROID_HOME/cmdline-tools/latest/bin/apkanalyzer" ]; then
    APKANALYZER="$ANDROID_HOME/cmdline-tools/latest/bin/apkanalyzer"
else
    echo "ERROR: apkanalyzer not found."
    exit 1
fi

if [ -n "${ANDROID_HOME:-}" ] &&
   [ -d "$ANDROID_HOME/build-tools" ]; then

    LATEST_BUILD_TOOLS="$(
        ls -1 "$ANDROID_HOME/build-tools" |
        sort -V |
        tail -1
    )"

    APKSIGNER="$ANDROID_HOME/build-tools/$LATEST_BUILD_TOOLS/apksigner"
fi

if [ -z "${APKSIGNER:-}" ] || [ ! -x "$APKSIGNER" ]; then
    if command -v apksigner >/dev/null 2>&1; then
        APKSIGNER="$(command -v apksigner)"
    else
        echo "ERROR: apksigner not found."
        exit 1
    fi
fi

apk_manifest() {
    "$APKANALYZER" manifest print "$1"
}

get_package() {
    "$APKANALYZER" manifest application-id "$1"
}

get_version_name() {
    "$APKANALYZER" manifest version-name "$1"
}

get_version_code() {
    "$APKANALYZER" manifest version-code "$1"
}

get_min_sdk() {
    "$APKANALYZER" manifest min-sdk "$1"
}

get_target_sdk() {
    "$APKANALYZER" manifest target-sdk "$1"
}

get_signature() {
    "$APKSIGNER" verify --print-certs "$1" |
        grep "certificate SHA-256 digest:" |
        awk '{print $NF}'
}

get_permissions() {
    "$APKANALYZER" manifest permissions "$1" 2>/dev/null |
        sort
}

has_apk_file() {
    local apk="$1"
    local file="$2"

    unzip -l "$apk" 2>/dev/null |
        awk '{print $4}' |
        grep -Fx "$file" >/dev/null 2>&1
}

has_manifest_entry() {
    local manifest="$1"
    local pattern="$2"

    grep -q "$pattern" "$manifest"
}

check_apk_runtime_files() {
    local apk="$1"
    local failed=0

    local required_files=(
        "lib/arm64-v8a/libflutter.so"
        "assets/flutter_assets/isolate_snapshot_data"
        "assets/flutter_assets/kernel_blob.bin"
    )

    for file in "${required_files[@]}"; do
        if has_apk_file "$apk" "$file"; then
            echo "OK: Runtime file: $file"
        else
            echo "WARNING: Runtime file missing: $file"
            failed=1
        fi
    done

    return "$failed"
}

count_flutter_assets() {
    local apk="$1"

    unzip -l "$apk" 2>/dev/null |
        awk '{print $4}' |
        grep '^flutter_assets/' |
        wc -l
}

print_assets() {
    local apk="$1"

    unzip -l "$apk" 2>/dev/null |
        awk '{print $4}' |
        grep '^flutter_assets/' |
        sort
}

apk_info() {
    local apk="$1"

    echo "Package Name:"
    get_package "$apk"

    echo "Version Name:"
    get_version_name "$apk"

    echo "Version Code:"
    get_version_code "$apk"

    echo "Min SDK:"
    get_min_sdk "$apk"

    echo "Target SDK:"
    get_target_sdk "$apk"

    echo "Certificate SHA-256:"
    get_signature "$apk"

    echo "Permissions:"
    get_permissions "$apk"

    echo "Flutter Asset Count:"
    count_flutter_assets "$apk"
}

echo "=========================================="
echo "2FUN APK RELEASE DIAGNOSTIC"
echo "=========================================="
echo

echo "NEW APK"
echo "------------------------------------------"
echo "File: $NEW_APK"
apk_info "$NEW_APK"
echo

FAILED=0
WARNING=0

echo "NEW APK MANIFEST"
echo "------------------------------------------"
apk_manifest "$NEW_APK" > /tmp/2fun_new_manifest.txt

if has_manifest_entry /tmp/2fun_new_manifest.txt 'android:name="android.app.Application"'; then
    echo "WARNING: Custom android.app.Application detected"
    WARNING=1
else
    echo "OK: No unexpected android.app.Application override"
fi

if has_manifest_entry /tmp/2fun_new_manifest.txt 'android:name="io.flutter.app.FlutterApplication"'; then
    echo "FAILED: Legacy FlutterApplication detected"
    FAILED=1
else
    echo "OK: FlutterApplication embedding is not legacy"
fi

if has_manifest_entry /tmp/2fun_new_manifest.txt 'android:name="flutterEmbedding"'; then
    echo "OK: Flutter embedding metadata present"
else
    echo "FAILED: Flutter embedding metadata missing"
    FAILED=1
fi

if has_manifest_entry /tmp/2fun_new_manifest.txt 'android.intent.action.MAIN'; then
    echo "OK: MAIN launcher activity present"
else
    echo "FAILED: MAIN launcher activity missing"
    FAILED=1
fi

if has_manifest_entry /tmp/2fun_new_manifest.txt 'android.intent.category.LAUNCHER'; then
    echo "OK: LAUNCHER category present"
else
    echo "FAILED: LAUNCHER category missing"
    FAILED=1
fi

if grep -q 'android.permission.INTERNET' /tmp/2fun_new_manifest.txt; then
    echo "Permission: INTERNET"
else
    echo "Permission: INTERNET not declared"
fi

if grep -q 'android.permission.ACCESS_NETWORK_STATE' /tmp/2fun_new_manifest.txt; then
    echo "Permission: ACCESS_NETWORK_STATE"
else
    echo "Permission: ACCESS_NETWORK_STATE not declared"
fi

echo
echo "ANDROID RUNTIME FILES"
echo "------------------------------------------"

if check_apk_runtime_files "$NEW_APK"; then
    echo "OK: Required Flutter runtime files present"
else
    echo "WARNING: One or more Flutter runtime files are missing"
    WARNING=1
fi

echo
echo "CRITICAL FLUTTER ASSETS"
echo "------------------------------------------"

CRITICAL_ASSETS=(
    "flutter_assets/assets/images/logo/logo.png"
    "flutter_assets/assets/translations/fa.json"
    "flutter_assets/assets/translations/en.json"
    "flutter_assets/assets/translations/ar.json"
    "flutter_assets/assets/data/countries.json"
)

for asset in "${CRITICAL_ASSETS[@]}"; do
    if has_apk_file "$NEW_APK" "$asset"; then
        echo "OK: $asset"
    else
        echo "FAILED: Missing asset: $asset"
        FAILED=1
    fi
done

echo
echo "FLUTTER ASSET SUMMARY"
echo "------------------------------------------"
echo "Total Flutter assets: $(count_flutter_assets "$NEW_APK")"

if [ "$#" -eq 1 ]; then
    echo
    echo "=========================================="
    echo "RESULT"
    echo "=========================================="

    if [ "$FAILED" -ne 0 ]; then
        echo "FAILED"
        exit 1
    fi

    echo "VALIDATED"
    echo
    echo "New APK structural diagnostic completed."
    exit 0
fi

echo
echo "OLD APK"
echo "------------------------------------------"
echo "File: $OLD_APK"
apk_info "$OLD_APK"
echo

OLD_PACKAGE="$(get_package "$OLD_APK")"
NEW_PACKAGE="$(get_package "$NEW_APK")"

OLD_VERSION_NAME="$(get_version_name "$OLD_APK")"
NEW_VERSION_NAME="$(get_version_name "$NEW_APK")"

OLD_VERSION_CODE="$(get_version_code "$OLD_APK")"
NEW_VERSION_CODE="$(get_version_code "$NEW_APK")"

OLD_MIN_SDK="$(get_min_sdk "$OLD_APK")"
NEW_MIN_SDK="$(get_min_sdk "$NEW_APK")"

OLD_TARGET_SDK="$(get_target_sdk "$OLD_APK")"
NEW_TARGET_SDK="$(get_target_sdk "$NEW_APK")"

OLD_SIGNATURE="$(get_signature "$OLD_APK")"
NEW_SIGNATURE="$(get_signature "$NEW_APK")"

echo "COMPARISON"
echo "------------------------------------------"

if [ "$OLD_PACKAGE" != "$NEW_PACKAGE" ]; then
    echo "FAILED: Package Name mismatch"
    echo "  Old: $OLD_PACKAGE"
    echo "  New: $NEW_PACKAGE"
    FAILED=1
else
    echo "OK: Package Name"
fi

if [ "$OLD_SIGNATURE" != "$NEW_SIGNATURE" ]; then
    echo "FAILED: Signature mismatch"
    echo "  Old: $OLD_SIGNATURE"
    echo "  New: $NEW_SIGNATURE"
    FAILED=1
else
    echo "OK: Signature"
fi

if [ "$NEW_VERSION_CODE" -lt "$OLD_VERSION_CODE" ] 2>/dev/null; then
    echo "FAILED: Version downgrade"
    echo "  Old: $OLD_VERSION_CODE"
    echo "  New: $NEW_VERSION_CODE"
    FAILED=1
else
    echo "OK: Version Code"
fi

if [ "$OLD_VERSION_NAME" != "$NEW_VERSION_NAME" ]; then
    echo "WARNING: Version Name changed"
    echo "  Old: $OLD_VERSION_NAME"
    echo "  New: $NEW_VERSION_NAME"
    WARNING=1
else
    echo "OK: Version Name"
fi

if [ "$OLD_MIN_SDK" != "$NEW_MIN_SDK" ]; then
    echo "WARNING: Min SDK changed"
    echo "  Old: $OLD_MIN_SDK"
    echo "  New: $NEW_MIN_SDK"
    WARNING=1
else
    echo "OK: Min SDK"
fi

if [ "$OLD_TARGET_SDK" != "$NEW_TARGET_SDK" ]; then
    echo "WARNING: Target SDK changed"
    echo "  Old: $OLD_TARGET_SDK"
    echo "  New: $NEW_TARGET_SDK"
    WARNING=1
else
    echo "OK: Target SDK"
fi

echo
echo "PERMISSION COMPARISON"
echo "------------------------------------------"

OLD_PERMISSIONS="$(get_permissions "$OLD_APK")"
NEW_PERMISSIONS="$(get_permissions "$NEW_APK")"

if [ "$OLD_PERMISSIONS" = "$NEW_PERMISSIONS" ]; then
    echo "OK: Permissions unchanged"
else
    echo "WARNING: Permissions changed"
    WARNING=1

    echo
    echo "Old permissions:"
    echo "$OLD_PERMISSIONS"

    echo
    echo "New permissions:"
    echo "$NEW_PERMISSIONS"
fi

echo
echo "FLUTTER ASSET COMPARISON"
echo "------------------------------------------"

OLD_ASSETS="$(mktemp)"
NEW_ASSETS="$(mktemp)"

print_assets "$OLD_APK" > "$OLD_ASSETS"
print_assets "$NEW_APK" > "$NEW_ASSETS"

if diff -u "$OLD_ASSETS" "$NEW_ASSETS" >/tmp/2fun_asset_diff.txt; then
    echo "OK: Flutter assets unchanged"
else
    echo "WARNING: Flutter asset set changed"
    WARNING=1
    cat /tmp/2fun_asset_diff.txt
fi

rm -f "$OLD_ASSETS" "$NEW_ASSETS"

echo
echo "CRITICAL ASSET COMPARISON"
echo "------------------------------------------"

for asset in "${CRITICAL_ASSETS[@]}"; do
    if has_apk_file "$OLD_APK" "$asset" &&
       has_apk_file "$NEW_APK" "$asset"; then
        echo "OK: $asset"
    elif ! has_apk_file "$OLD_APK" "$asset"; then
        echo "WARNING: Old APK missing: $asset"
        WARNING=1
    else
        echo "FAILED: New APK missing: $asset"
        FAILED=1
    fi
done

echo
echo "=========================================="
echo "RESULT"
echo "=========================================="

if [ "$FAILED" -ne 0 ]; then
    echo "FAILED"
    exit 1
elif [ "$WARNING" -ne 0 ]; then
    echo "WARNING"
    exit 0
else
    echo "COMPATIBLE"
    exit 0
fi
