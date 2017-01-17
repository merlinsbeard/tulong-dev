from message.models import Message
from django.views.generic import DetailView, ListView

class MessageList(ListView):
	model = Message
	template_name = "message_list.html"

	def get_queryset(self):
		queryset = super(MessageList, self).get_queryset()
		return queryset.filter(receiver=self.request.user.person)

class MessageDetail(DetailView):
	model = Message
	template_name = "message_detail.html"

    