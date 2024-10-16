from groceries.models import DietaryDetail

class UserService:
    @staticmethod
    def update_user_profile(user, data):
        logger.info(f"Updating user profile for user {user.id}")
        logger.info(f"Received data: {data}")

        # Update User fields
        if 'first_name' in data:
            user.first_name = data['first_name']
            logger.info(f"Updated first_name to {user.first_name}")
        if 'last_name' in data:
            user.last_name = data['last_name']
            logger.info(f"Updated last_name to {user.last_name}")
        if 'image' in data:
            user.image = data['image']
            logger.info(f"Updated image to {user.image}")

        user.save()
        logger.info("User data saved")

        # Update UserProfile fields if profile exists and data is provided
        profile_data = data.get('profile')
        if profile_data and hasattr(user, 'userprofile'):
            profile = user.userprofile
            if 'profile_pic' in profile_data:
                profile.profile_pic = profile_data['profile_pic']
                logger.info(f"Updated profile_pic to {profile.profile_pic}")
            if 'gender' in profile_data:
                profile.gender = profile_data['gender']
                logger.info(f"Updated gender to {profile.gender}")
            if 'dietary_requirements' in profile_data:
                dietary_ids = profile_data['dietary_requirements']
                profile.dietary_requirements.set(DietaryDetail.objects.filter(id__in=dietary_ids))
                logger.info(f"Updated dietary_requirements to {profile.dietary_requirements.all()}")

            profile.save()
            logger.info("Profile data saved")
        else:
            logger.info("No profile data provided or user has no profile, skipping profile update")

        return user