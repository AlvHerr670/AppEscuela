from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Remitente")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Destinatario")
    subject = models.CharField(max_length=255, blank=True, null=True, verbose_name="Asunto") 
    body = models.TextField(verbose_name="Cuerpo del mensaje")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    is_read = models.BooleanField(default=False, verbose_name="Leído")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return f'De: {self.sender.username} - Para: {self.receiver.username} - Asunto: {self.subject or "Sin Asunto"} - Fecha: {self.timestamp.strftime("%Y-%m-%d %H:%M")}'
