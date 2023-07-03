$(document).ready(function() {
    $('.animated-label input').each(function() {
        $(this).on('focusin', function() {
            $(this).parent().find('label').addClass('active');
        });
        $(this).on('keydown', function() {
            $(this).parent().find('label').addClass('active');
        });
        $(this).on('focusout', function() {
            if(!this.value) {
                $(this).parent().find('label').removeClass('active');
            }
        })
        if(this.value) {
            $(this).parent().find('label').addClass('active');
        }
    })
    $('.animated-label select').each(function() {
        $(this).on('focusin', function() {
            $(this).parent().parent().find('label').addClass('active');
        });
        $(this).on('focusout', function() {
            if(!this.value) {
                $(this).parent().parent().find('label').removeClass('active');
            }
        })
        if(this.value) {
            $(this).parent().parent().find('label').addClass('active');
        }
    })
})

function close_with_x_change(self) {
    if(!self.children('option:first-child').is(':selected') && !self.parent().find('.delete-select').length) {
        const $delete_select = $('<span></span>')
        $delete_select.attr({
            'class': 'delete-select text-danger',
            // 'style': 'right: 10px; top: 50%; cursor: pointer; font-size: 24px;',
        })

        const $close_icon = $('<button></button>')
        $close_icon.attr({
            'type': 'button',
            'class': 'close',
            'aria-label': 'Close',
        })

        const $close_icon_span = $('<span></span>').html('&times;')
        $close_icon_span.attr({ 'aria-hidden': 'true', })

        $close_icon.append($close_icon_span)
        $delete_select.append($close_icon)

        self.parent().append($delete_select)

        $delete_select.click(function() {
            self.change(self.prop('selectedIndex', 0));
            $(this).parent().parent().find('label').removeClass('active')
            $(this).remove()
        })
    }
}
function close_with_x() {
    $('.close-with-x').each(function() {
        const self = $(this)
        close_with_x_change(self)

        self.change(function() {
            close_with_x_change(self)
        })
    })
}

function setCookie(cname, cvalue, exdays) {
    let d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    const expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function deleteCookie(cname) {
    setCookie(cname, '', 0)
}

function getCookie(cname) {
    const name = cname + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}