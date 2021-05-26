import xbmc


def get_user_input(**kwargs):
    # default text, heading, hidden
    keyboard = xbmc.Keyboard(kwargs['placeholder'] if 'placeholder' in kwargs else '', kwargs['prompt'])
    keyboard.doModal()
    
    if not keyboard.isConfirmed():
        # user hit cancel
        return None
        
    return keyboard.getText()