# transaction/services.py

def update_status_device(transaction, device):
    if transaction.type == 'ENTRY':
        device.status_device = 'IN_STOCK'
    elif transaction.type == 'OUTPUT':
        device.status_device = 'ASSIGNED'
    elif transaction.type == 'SUPPORT':
        device.status_device = 'IN_SUPPORT'
    device.save()
