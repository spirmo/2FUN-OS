class ConflictResolver:

    def check(self, local_data, remote_data):

        conflicts = []

        for key in local_data:
            if key in remote_data:
                if local_data[key] != remote_data[key]:
                    conflicts.append(key)

        return {
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts
        }
