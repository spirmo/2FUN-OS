========================================================
2FUN SUPER APP
FLUTTER MVP STRUCTURE
ARCHITECTURE LOCKED
========================================================

STATUS
LOCKED

PURPOSE

This snapshot defines the Flutter architecture for the first executable MVP.

========================================================
ROOT
========================================================

lib/

    app/
        app.dart

    core/
        constants/
        theme/
        services/
        routing/

    shared/
        widgets/

    features/

        auth/

        dashboard/

        knowledge/

        wizard/

========================================================
FIRST MVP FEATURES
========================================================

✔ Login

✔ Dashboard

✔ Knowledge Production

✔ Wizard

========================================================
WIZARD STEPS
========================================================

1 Canonical Name

2 Short Description

3 Definitions

4 Evidence

5 Aliases

6 Relationships

7 Review

8 Save Draft

9 Submit

========================================================
RULES
========================================================

Feature Based Architecture

Shared Widgets only inside shared/

Business Logic stays inside feature

No feature may directly depend on another feature

Navigation starts from app.dart

========================================================
NEXT PHASE
========================================================

Login

Dashboard

Knowledge

Wizard

========================================================
END
========================================================
