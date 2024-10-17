from groceries.models import DietaryDetail
import logging

logger = logging.getLogger(__name__)

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
        if 'gender' in data:
            user.gender = data['gender']
            logger.info(f"Updated gender to {user.gender}")
        if 'dietary_requirements' in data:
            dietary_ids = data['dietary_requirements']
            user.dietary_requirements.set(DietaryDetail.objects.filter(id__in=dietary_ids))
            logger.info(f"Updated dietary_requirements to {user.dietary_requirements.all()}")

        user.save()
        logger.info("User data saved")

        return user