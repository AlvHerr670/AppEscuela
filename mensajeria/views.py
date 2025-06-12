from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q 
from .models import Message
from django.contrib.auth.models import User

@login_required
def inbox(request):

    received_messages = Message.objects.filter(receiver=request.user).select_related('sender').order_by('-timestamp')
    context = {
        'received_messages': received_messages,
        'page_title': 'Bandeja de Entrada',
    }
    return render(request, 'mensajeria/inbox.html', context)

@login_required
def compose_message(request, recipient_username=None):
    recipient = None
    if recipient_username:
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            messages.error(request, "El usuario destinatario no existe.")
            return redirect('compose_message')
    
    users = User.objects.exclude(id=request.user.id).order_by('username')

    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            messages.error(request, "El destinatario especificado no existe.")
            context = {
                'users': users,
                'page_title': 'Escribir Mensaje',
                'error': True,
                'subject_value': subject, 
                'body_value': body,       
                'selected_receiver_id': receiver_id 
            }
            return render(request, 'mensajeria/compose.html', context)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            body=body
        )
        messages.success(request, "Mensaje enviado exitosamente.")
        return redirect('inbox')

    context = {
        'recipient': recipient,
        'users': users, 
        'page_title': 'Escribir Mensaje',
        'subject_value': '',
        'body_value': '',
        'selected_receiver_id': recipient.id if recipient else ''
    }
    return render(request, 'mensajeria/compose.html', context)

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, Q(id=message_id) & Q(sender=request.user) | Q(receiver=request.user))

    if request.user == message.receiver and not message.is_read:
        message.is_read = True
        message.save()

    context = {
        'message': message,
        'page_title': f'Mensaje de {message.sender.username}',
    }
    return render(request, 'mensajeria/view_message.html', context)

@login_required
def conversation(request, user_id_other):
    other_user = get_object_or_404(User.objects.select_related('avatar'), id=user_id_other)

    messages_in_conversation = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) |
         Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp').select_related('sender', 'receiver')

    Message.objects.filter(receiver=request.user, sender=other_user, is_read=False).update(is_read=True)


    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                body=body,
                subject=f'Re: Conversación con {other_user.username}' 
            )
            return redirect('conversation', user_id_other=user_id_other)
        else:
            messages.error(request, "El mensaje no puede estar vacío.")

    context = {
        'other_user': other_user,
        'messages': messages_in_conversation,
        'page_title': f'Conversación con {other_user.username}',
    }
    return render(request, 'mensajeria/conversation.html', context)