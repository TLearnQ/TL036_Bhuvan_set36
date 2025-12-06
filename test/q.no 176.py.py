
get firewall_rules = []

def fw_router(request):
    parts = request.split()
    if len(parts) < 2:
        return "Incorrect Request"
    
    