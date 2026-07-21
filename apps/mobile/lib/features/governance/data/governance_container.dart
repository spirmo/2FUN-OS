import '../../../../../../engines/governance/core/governance_controller.dart';

import 'governance_api_service.dart';
import 'governance_repository.dart';


class GovernanceContainer {

  static final GovernanceRepository repository =
      GovernanceRepository(
        apiService: GovernanceApiService(
          controller: GovernanceController(),
        ),
      );

}
