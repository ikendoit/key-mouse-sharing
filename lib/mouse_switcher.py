from pynput.mouse import Button

def switch_button(button):
    return {
        Button.left: 'left',
        Button.right: 'right'
    }.get(button, None)
    
