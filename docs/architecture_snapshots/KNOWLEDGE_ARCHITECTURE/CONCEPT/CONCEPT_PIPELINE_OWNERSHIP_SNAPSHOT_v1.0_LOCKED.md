============================================================
2FUN-OS
CONCEPT OWNERSHIP ARCHITECTURE SNAPSHOT
============================================================

Proposed Filename:
CONCEPT_PIPELINE_OWNERSHIP_SNAPSHOT_v1.0_LOCKED.md

Proposed Architecture Snapshot Folder:
00_ARCHITECTURE_SNAPSHOTS/
   KNOWLEDGE/
      CONCEPT/
         CONCEPT_PIPELINE_OWNERSHIP_SNAPSHOT_v1.0_LOCKED.md

Status:
LOCKED

Purpose:
تعریف مالکیت دقیق تمام مراحل و مسئولیت‌های Concept Pipeline
بین User App، Core App، Concept Engine و سایر موتورهای مستقل.

============================================================
1. ARCHITECTURAL PRINCIPLE
============================================================

اصل پایه:

هیچ‌کدام از User App و Core App مالک Persistence یا Database
برای Concept نیستند.

Concept Engine تنها درگاه و مالک Persistence مربوط به Concept
است و مسئول:

- دریافت داده
- ثبت Concept
- Versioning
- History
- Approval State
- هماهنگی جریان Concept
- انتقال Concept تأییدشده به Knowledge Engine

است.

User App و Core App فقط از طریق Concept Engine با Concept کار
می‌کنند.

============================================================
2. CONCEPT PIPELINE
============================================================

Concept Creation
        ↓
Concept Completion
        ↓
Validation
        ↓
Initial Submission
        ↓
Core Review
        ↓
Approve / Reject
        ↓
Continue Completion
        ↓
Final Completion
        ↓
Final Core Approval
        ↓
Concept Engine Handoff
        ↓
Knowledge Engine
        ↓
Knowledge Publication


============================================================
3. ITEM OWNERSHIP
============================================================

Concept Visible Items:

User App:
36 Items
- Mandatory Items
- Optional Items

Core App:
47 Items
- Mandatory Items
- Optional Items
- System Items

User App may optionally display System Items when needed,
but System Items are not required for the User App's normal
36-item Concept workflow.

Core App must have access to all 47 Concept Items.

IMPORTANT:

وجود یک Item در یک Application به معنی مالکیت آن Application
بر آن Item نیست.

Concept Engine remains the canonical Concept authority.


============================================================
4. CONCEPT CREATION
============================================================

Primary Owner:
User App

Role:
- ایجاد Concept
- شروع Concept
- ورود داده‌های اولیه

Concept Engine:
- دریافت Concept
- اعتبارسنجی ساختاری اولیه
- ایجاد/مدیریت Concept داخلی
- Persistence

Core App:
No ownership.


============================================================
5. CONCEPT COMPLETION
============================================================

Primary Owner:
User App

Role:
- تکمیل 36 Item
- تکمیل Mandatory Items
- تکمیل Optional Items
- ارسال اطلاعات تکمیل‌شده

Concept Engine:
- دریافت تغییرات
- نگهداری وضعیت
- Persistence
- Versioning
- History
- اعلام تغییرات لازم به موتورهای تخصصی

Core App:
- فقط مشاهده و بررسی در مراحل مربوط به خود.


============================================================
6. MANDATORY INITIAL COMPLETION
============================================================

User App:
مسئول تکمیل 11 Mandatory Items.

Concept Engine:
- ثبت وضعیت تکمیل
- Validation
- Persistence
- آماده‌سازی برای Submission

Core App:
- مشاهده
- بررسی
- تصمیم Approval / Rejection


============================================================
7. VALIDATION
============================================================

Primary Owner:
Validation Engine

Validation Engine:
- بررسی اعتبار Concept
- بررسی ساختار
- بررسی الزامات
- تولید Validation Result

Concept Engine:
- فراخوانی Validation Engine
- دریافت نتیجه
- ثبت نتیجه
- استفاده از نتیجه در Pipeline

User App:
- نمایش نتیجه

Core App:
- نمایش نتیجه

Neither User App nor Core App owns validation logic.


============================================================
8. SUBMISSION
============================================================

Initiator:
User App

Canonical Coordinator:
Concept Engine

Flow:

User App
   ↓
Concept Engine
   ↓
Validation
   ↓
Lifecycle
   ↓
Approval Queue / Review Flow


User App owns the action of submitting.

Concept Engine owns the canonical submission process
and persistence.

Core App does not create the submission.


============================================================
9. CORE REVIEW
============================================================

Primary Application:
Core App

Purpose:
بررسی Concept ارسال‌شده توسط User.

Core App:
- نمایش Concept
- نمایش تمام 47 Items
- نمایش Validation
- نمایش وضعیت
- ارائه امکان Approve / Reject در محدوده اختیار

Concept Engine:
- تأمین داده
- هماهنگی فرآیند
- ثبت نتیجه

Core App does NOT own Concept persistence.


============================================================
10. APPROVE / REJECT
============================================================

Primary Application Owner:
Core App

Authority:
Governance / Permission System

Lifecycle Rule Owner:
Lifecycle Engine

Canonical Concept Coordinator:
Concept Engine

Flow:

Core App
   ↓
Authority Check
   ↓
Lifecycle Validation
   ↓
Concept Engine
   ↓
State Change


Governance determines:
"Who is allowed to approve/reject?"

Lifecycle Engine determines:
"Is this state transition allowed?"

Concept Engine coordinates and persists the result.

User App has no approval authority.


============================================================
11. REVIEWER / DECISION-MAKER AUTHORITY
============================================================

Primary Owner:
Reviewer Authority / Decision Authority Mechanism

Implementation:
Existing suitable engine should be reused if possible.

If no suitable engine exists:
Create a dedicated engine.

Responsibilities:

- Identify reviewer
- Track reviewer decisions
- Calculate decision accuracy
- Track correct/incorrect decisions
- Calculate reviewer authority/reliability
- Apply configurable minimum threshold
- Suspend/restrict approval/rejection authority when
  reviewer performance crosses the defined red line

Example:

Reviewer A
Accuracy = 70%
Minimum Required = 80%

Result:
Approve / Reject Authority = SUSPENDED


Reviewer B
Accuracy = 100%

Result:
Approve / Reject Authority = ACTIVE


IMPORTANT:

This mechanism is NOT owned by:
- User App
- Core App
- Concept Engine
- Validation Engine
- Lifecycle Engine

Concept Engine only consumes the resulting authority decision.

Implementation of this mechanism will be determined AFTER
completion of the ownership architecture review.


============================================================
12. DECISION IDENTITY / ACCOUNTABILITY
============================================================

Every approval/rejection must preserve:

- Concept ID
- Concept Code
- Concept Version
- Decision Type
- Decision Maker
- Decision Time
- Authority/Reviewer Status
- Decision Result
- Rejection Reason when applicable

Purpose:
Traceability and accountability.

Concept Engine:
Owns the Concept-side persistence of this decision record.

Governance:
Owns authority identity.

Decision Authority Mechanism:
Owns reviewer performance/authority calculation.


============================================================
13. CONCEPT STATUS / LIFECYCLE
============================================================

Primary Rule Owner:
Lifecycle Engine

Lifecycle Engine owns:

- Allowed states
- Allowed transitions
- Transition rules
- Lifecycle validity

Examples:

PENDING_REVIEW → APPROVED
PENDING_REVIEW → REJECTED

must be validated by Lifecycle Engine.

Lifecycle Engine does NOT determine:
- Who the reviewer is
- Whether reviewer has authority
- Reviewer reputation


============================================================
14. COMPLETENESS
============================================================

Primary Owner:
Completeness Mechanism

Responsibilities:

- Calculate Concept completeness
- Determine completion percentage
- Detect completion of required items
- Produce completeness result

Concept Engine:
- requests calculation
- receives result
- records result
- exposes result

User App:
- displays result

Core App:
- displays result

Neither application owns the calculation.


============================================================
15. SCORING / XP / REWARD DATA
============================================================

Primary Owner:
Scoring / Computational Mechanism

User App:
No scoring ownership.

Core App:
No scoring ownership.

Concept Engine:
- Announces relevant Concept changes to the scoring mechanism
- Receives calculated result
- Stores/records result where Concept history requires it
- Displays/serves result

Concept Engine does NOT own the scoring algorithm.

The scoring mechanism remains independent.


============================================================
16. FINAL COMPLETION
============================================================

User App:
Completes remaining Concept Items.

Concept Engine:
- receives changes
- validates
- calculates/requests completeness
- persists state
- maintains version/history

Core App:
Reviews the completed Concept.


============================================================
17. FINAL CORE APPROVAL
============================================================

Final Approval belongs to:
Core Governance Workflow

Core App:
- displays Concept
- displays all 47 Items
- allows authorized Core member to approve/reject

Governance:
- verifies authority

Reviewer Authority Mechanism:
- verifies reviewer eligibility

Lifecycle Engine:
- verifies transition legality

Concept Engine:
- records and coordinates the final approval.


============================================================
18. END OF USER APP / CORE APP RESPONSIBILITY
============================================================

IMPORTANT LOCK:

After Final Approval:

User App responsibility = END

Core App responsibility = END

Neither application performs Publication.

Neither application owns Publication.

Neither application writes Publication data directly.


============================================================
19. HANDOFF TO KNOWLEDGE ENGINE
============================================================

After Final Approval:

Core App
   ↓
Final Approval
   ↓
Concept Engine
   ↓
Knowledge Engine


Concept Engine is responsible for:

- Detecting final approval
- Preparing canonical Concept data
- Handing the approved Concept to Knowledge Engine
- Ensuring identity/version continuity
- Recording the handoff result


============================================================
20. PUBLICATION
============================================================

Primary Owner:
Knowledge Engine

Knowledge Engine owns:

- Receiving approved Concept
- Knowledge integration
- Publication
- Knowledge-side state
- Knowledge availability

User App:
No publication ownership.

Core App:
No publication ownership.

Concept Engine:
Does NOT own publication.

Concept Engine only performs the canonical handoff.


============================================================
21. PERSISTENCE
============================================================

Primary Owner:
Concept Engine

User App:
NO Concept database ownership.

Core App:
NO Concept database ownership.

Knowledge Engine:
Owns Knowledge-side persistence after handoff,
but does not become owner of the Concept lifecycle itself.

Concept Engine remains the canonical persistence authority
for Concept data, versions and Concept history.


============================================================
22. VERSIONING
============================================================

Primary Owner:
Concept Engine

Responsibilities:

- Permanent Concept Code
- Concept Version
- Revision creation
- Version persistence
- Version history
- Identity preservation

User App:
May initiate a revision through Concept Engine.

Core App:
May review/approve/reject a revision through Concept Engine.

Neither application owns Versioning.


============================================================
23. HISTORY / AUDIT
============================================================

Concept History:
Owned by Concept Engine.

Governance decision history:
Must preserve reviewer identity and decision accountability.

EventBus:
Used to announce important Concept lifecycle events.

Concept Engine remains the canonical coordinator of
Concept-specific history.


============================================================
24. EVENT NOTIFICATION
============================================================

Primary Infrastructure:
EventBus

Concept Engine:
Emits Concept-related events.

Examples:

CONCEPT_CREATED
CONCEPT_SUBMITTED
CONCEPT_APPROVED
CONCEPT_REJECTED
CONCEPT_VERSION_CREATED
CONCEPT_COMPLETION_CHANGED
CONCEPT_FINAL_APPROVED
CONCEPT_KNOWLEDGE_HANDOFF


Other engines consume events according to their own ownership.


============================================================
25. FINAL OWNERSHIP MATRIX
============================================================

Function                         Owner
------------------------------------------------------------
Create Concept                   User App
Complete Concept                 User App
Display Concept                  User/Core
36 Visible Items                 User App
47 Items                         Core App
Validation Logic                Validation Engine
Submission Coordination         Concept Engine
Lifecycle Rules                 Lifecycle Engine
Reviewer Permission             Governance
Reviewer Authority              Authority Mechanism
Approve / Reject UI             Core App
Approval Persistence            Concept Engine
Rejection Persistence           Concept Engine
Completeness Calculation        Completeness Mechanism
Scoring Calculation             Scoring Mechanism
Concept Persistence              Concept Engine
Concept Versioning              Concept Engine
Concept History                 Concept Engine
Event Notification              EventBus
Final Approval                  Core Governance Workflow
Final Handoff                   Concept Engine
Knowledge Integration           Knowledge Engine
Publication                     Knowledge Engine


============================================================
26. NON-OWNERSHIP LOCK
============================================================

User App MUST NOT own:

- Concept Database
- Concept Persistence
- Versioning
- Approval Logic
- Rejection Logic
- Scoring Logic
- Completeness Logic
- Publication

Core App MUST NOT own:

- Concept Database
- Concept Persistence
- Versioning
- Validation Logic
- Lifecycle Rules
- Scoring Logic
- Completeness Logic
- Publication

Concept Engine MUST NOT own:

- Reviewer Authority Policy
- Scoring Algorithm
- Validation Rules
- Lifecycle Rules
- Knowledge Publication

Knowledge Engine MUST NOT own:

- User App workflow
- Core Approval UI
- Concept lifecycle authority


============================================================
27. FINAL ARCHITECTURAL PRINCIPLE
============================================================

User App = CREATE / COMPLETE / DISPLAY

Core App = REVIEW / APPROVE / REJECT / DISPLAY

Concept Engine = CANONICAL CONCEPT COORDINATION /
PERSISTENCE / VERSIONING / HISTORY / HANDOFF

Validation Engine = VALIDATION

Lifecycle Engine = LIFECYCLE RULES

Governance = AUTHORITY / PERMISSION

Reviewer Authority Mechanism = REVIEWER PERFORMANCE /
ELIGIBILITY

Completeness Mechanism = COMPLETENESS CALCULATION

Scoring Mechanism = SCORING CALCULATION

EventBus = EVENT DISTRIBUTION

Knowledge Engine = KNOWLEDGE INTEGRATION / PUBLICATION

============================================================
STATUS
============================================================

CONCEPT OWNERSHIP ARCHITECTURE:
LOCKED

Next Phase:
IMPLEMENTATION

Implementation must follow this ownership matrix and MUST NOT
move ownership back into User App or Core App merely for
implementation convenience.

============================================================
END OF SNAPSHOT
============================================================
