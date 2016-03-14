from push_notifications.models import APNSDevice

class Push:
	def sendMessage(self,status):
		device = APNSDevice.objects.all()
		if device is None:
			print('No Device')
		message = 'Home Fried Potatoes, Yo-nola Bar, Soup du Jour, More...'
		device.send_message(message)