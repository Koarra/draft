# Activities
activity_check = True  # Default to True if no activities present
if len(kyc_case.kyc_dataset.activities) > 0:  # Only check if activities exist
    for activity in kyc_case.kyc_dataset.activities:
        if False in self.check_activity(activity):  # Missing field(s)
            activity_check = False
            break