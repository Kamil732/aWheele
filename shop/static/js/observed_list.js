$.fn.add_observed_offer = function() {
    $(this).click(function(e) {
        if($(this).prop('tagName') != 'INPUT') e.preventDefault()
        product_url = $(this).attr('data-href')

        $.ajax({
            method: 'GET',
            url: product_url,
            dataType: 'json',
            success: data => {
                if(data['observed_list_name'] && data['product_id']) {
                    let observed_list = getCookie(data['observed_list_name'])
                    if(observed_list) setCookie(data['observed_list_name'], `${observed_list},${data['product_id']}`)
                    else setCookie(data['observed_list_name'], data['product_id'])
                }

                $(this).removeClass('add-observed-offer')
                $(this).addClass('remove-observed-offer')
                $(this).find('i').addClass('fas')
                $(this).find('i').removeClass('far')
                $(this).attr('title', 'remove from observed list')
                $(this).attr('data-href', data['remove_observed_offer'])
                $(this).find('.title').text('remove from observed list')
                $(this).off()
                $(this).remove_observed_offer()
            }
        })
    })
}
$.fn.remove_observed_offer = function() {
    $(this).click(function(e) {
        if($(this).prop('tagName') != 'INPUT') e.preventDefault()
        product_url = $(this).attr('data-href')

        $.ajax({
            method: 'GET',
            url: product_url,
            dataType: 'json',
            success: data => {
                if(data['observed_list_name'] && data['product_id']) {
                    let observed_list = getCookie(data['observed_list_name'])
                    const observed_list_array = observed_list.split(',')
                    if (observed_list_array[0] == data['product_id']) {
                        if (observed_list_array.length == 1) deleteCookie(data['observed_list_name'])
                        else setCookie(data['observed_list_name'], observed_list.replace(data['product_id'] + ',', ''))
                    }
                    else setCookie(data['observed_list_name'], observed_list.replace(',' + data['product_id'], ''))
                }

                $(this).removeClass('remove-observed-offer')
                $(this).addClass('add-observed-offer')
                $(this).find('i').addClass('far')
                $(this).find('i').removeClass('fas')
                $(this).attr('title', 'add to observed list',)
                $(this).attr('data-href', data['add_observed_offer'],)
                $(this).find('.title').text('add to observed list')
                $(this).off()
                $(this).add_observed_offer()
            }
        })
    })
}

$(document).ready(function() {
    $('.add-observed-offer').each(function() {
        $(this).add_observed_offer()
    })
    $('.remove-observed-offer').each(function() {
        $(this).remove_observed_offer()
    })
})