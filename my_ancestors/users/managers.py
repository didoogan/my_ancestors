from django.contrib.auth.base_user import BaseUserManager


# class CustomManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, first_name, last_name, password, **extra_fields):
#         """
#         Creates and saves a User with the given first_name, last_name, email and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         first_name = self.model.normalize_username(first_name)
#         last_name = self.model.normalize_username(last_name)
#         user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, first_name=None, last_name=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, first_name, last_name, password, **extra_fields)
#
#     def create_superuser(self, email, first_name, last_name, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(email, first_name, last_name, password, **extra_fields)

class CustomManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
