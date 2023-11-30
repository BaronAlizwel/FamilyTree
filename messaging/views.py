from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MessageForm

def send_message(request, user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = CustomUser.objects.get(id=user_id)
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

def view_conversation(request, user_id):
    messages = Message.objects.filter(sender__id=user_id, recipient=request.user) | \
                Message.objects.filter(sender=request.user, recipient__id=user_id)
    return render(request, 'messaging/view_conversation.html', {'messages': messages})


@login_required
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            message = Message(sender=request.user, recipient=recipient, subject=subject, text=text)
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('messaging:inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/compose_message.html', {'form': form})


@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'received_messages': received_messages})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'sent_messages': sent_messages})

@login_required
def message_thread(request, message_id):
    message = Message.objects.get(pk=message_id)
    # Mark the message as read when viewed by the recipient
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/message_thread.html', {'message': message})
