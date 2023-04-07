function getURLParameter(sUrl, sParam) {
    let sPageURL = sUrl.substring(sUrl.indexOf('?') + 1);
    let sURLVariables = sPageURL.split('&');
    for (let i = 0; i < sURLVariables.length; i++) {
        let sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

class Index {
 
    static initPaginator() {
        document.body.querySelectorAll('.pagination > li > a')
                .forEach( link => link.addEventListener('click', Index.pagination_link_clickHandler) );
    }
 
    static pagination_link_clickHandler(event){
        event.preventDefault();
 
        let path = event.target.href;
        let page = getURLParameter(path, 'page');
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(page);
 
        if (typeof page !== 'undefined') {
            jQuery.ajax({
                url: jQuery(this).attr('action'),
                type: 'POST',
                data: {
                    'page': getURLParameter(path, 'page'),
                    csrfmiddlewaretoken:csrf
                },
                success : function (json) {
                    if (json.result)
                    {
                        console.log(json.comms);
                        console.log("Success!");
                        window.history.pushState({route: path}, "EVILEG", path);
                        jQuery("#comms_list").replaceWith(json.comms);
                        Index.initPaginator();
                        jQuery(window).scrollTop(jQuery(window).height());
                    }
                }
            });
        }
    }
}
 
Index.initPaginator();