from django.http import JsonResponse
from django.views import View

from scrapper.message import SendMessages
from scrapper.models import LinkedInProfile
from scrapper.profile import Profiles


class Testing(View):
    def get(self, request):
        response = {
            "message": "Sameer Kumar"
        }

        return JsonResponse(response)


class ListOfAllProfiles(View):
    @staticmethod
    def get(request):
        profiles = LinkedInProfile.objects.all()

        items = []
        for profile in profiles:
            items.append({
                "fullName": profile.fullName,
                "jobTitle": profile.jobTitle,
                "status": profile.status
            })

        response = {
            "count": len(items),
            "data": items
        }

        return JsonResponse(response)


print("1. Linked In Profile")
print("2. Send Message")
print("3. (Or any other) Exit")

choice = int(input("Enter choice: "))

if choice == 1:
    profile = Profiles()
    profile.run()
    profile.close_session()

elif choice == 2:
    send_message = SendMessages()
    send_message.run()
    send_message.close_session()

else:
    print("Exit.")
