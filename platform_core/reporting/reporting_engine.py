import time
import json


class ReportingEngine:

    def __init__(self):

        self.reports = []

    # -----------------------------------
    # Generate Report
    # تولید گزارش
    # -----------------------------------

    def generate(self, event):

        source = event.get("source", "UNKNOWN")

        identity = event.get("identity", {})

        behavior = event.get("behavior", {})

        risk = event.get("risk", {})

        governance = event.get("governance", {})

        memory = event.get("memory", {})

        # -----------------------------------
        # Human Report
        # گزارش انسانی
        # -----------------------------------

        human_report = {
            "summary": f"User {source} triggered event with identity {identity.get('identity')}",
            "risk_level": risk.get("risk_level"),
            "trust_level": governance.get("trust_level"),
            "stability": behavior.get("stability_score"),
            "governance_score": governance.get("governance_score"),
            "time": time.ctime(),
        }

        # -----------------------------------
        # Machine Report
        # گزارش ماشینی
        # -----------------------------------

        machine_report = {
            "source": source,
            "identity": identity,
            "behavior": behavior,
            "risk": risk,
            "governance": governance,
            "memory": memory,
            "timestamp": time.time(),
        }

        # -----------------------------------
        # Store
        # ذخیره
        # -----------------------------------

        report = {"human": human_report, "machine": machine_report}

        self.reports.append(report)

        return report

    # -----------------------------------
    # Export JSONL
    # خروجی JSONL (برای لاگ)
    # -----------------------------------

    def export_jsonl(self, file_path):

        with open(file_path, "w", encoding="utf-8") as f:

            for r in self.reports:

                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        return {"status": "exported", "file": file_path, "count": len(self.reports)}
