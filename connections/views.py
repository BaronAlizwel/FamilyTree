from django.shortcuts import render, redirect
from .models import Connection, ConnectionRequest
from .forms import ConnectionForm
from django.contrib.auth.decorators import login_required


def create_connection(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_connections')
    else:
        form = ConnectionForm()
    return render(request, 'connections/create_connection.html', {'form': form})


def accept_connection_request(request, request_id):
    connection_request = ConnectionRequest.objects.get(id=request_id)
    connection_request.status = ConnectionRequest.ACCEPTED
    connection_request.save()
    return redirect('view_connections')


def reject_connection_request(request, request_id):
    connection_request = ConnectionRequest.objects.get(id=request_id)
    connection_request.status = ConnectionRequest.REJECTED
    connection_request.save()
    return redirect('view_connections')


def edit_connection(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    if request.method == 'POST':
        form = ConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            return redirect('connections')
    else:
        form = ConnectionForm(instance=connection)
    return render(request, 'connections/edit_connection.html', {'form': form})


def delete_connection(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    connection.delete()
    return redirect('connections')


# def view_connections(request):
#     connections = Connection.objects.filter(from_user=request.user)
#     return render(request, 'connections/view_connections.html', {'connections': connections})

@login_required
def view_connections(request):
    if request.method == 'POST':
        connection_request_id = request.POST.get('connection_request_id')
        connection_request = ConnectionRequest.objects.get(id=connection_request_id)
        if connection_request.to_user == request.user:
            if request.POST.get('accept'):
                # Accept the connection request
                Connection.objects.create(from_user=connection_request.from_user, to_user=connection_request.to_user)
                connection_request.status = ConnectionRequest.ACCEPTED
                connection_request.save()
            elif request.POST.get('reject'):
                # Reject the connection request
                connection_request.status = ConnectionRequest.REJECTED
                connection_request.save()
            return redirect('view_connections')
    else:
        user = request.user
        connections = Connection.objects.filter(from_user=user)
        connection_requests = ConnectionRequest.objects.filter(to_user=user, status=ConnectionRequest.PENDING)
        return render(request, 'connections/view_connections.html', {'connections': connections, 'connection_requests': connection_requests})


@login_required
def view_family_tree(request):
    user = request.user
    family_tree = user.get_family_tree()
    return render(request, 'connections/family_tree.html', {'family_tree': family_tree})
