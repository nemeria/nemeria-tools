$(function() {
    $('form').children().change(function() {
        if ($('input[name=drawall]').prop("checked")==true) { $('input[name=alliances]').hide() }
        else { $('input[name=alliances]').show() }
        var src="";
        src+="monde="+document.carteform.monde.value;
        if (document.carteform.drawall.checked==true) {
            src+="&drawall=1";
        }
        if (document.carteform.alliances.value != "") {
            for (a in document.carteform.alliances.value.split(/,\s*/)) {
                src+="&alliance="+document.carteform.alliances.value.split(/,\s*/)[a];
            }
        }
        src+="&h="+(Math.floor($(document).width()-$(document).width()/12*4));
        xpos=$('input[name=xpos]').prop('value');
        ypos=$('input[name=ypos]').prop('value');
        if (isNaN(xpos)) { xpos="0" }
        if (isNaN(ypos)) { ypos="0" }
        zoom=parseInt($('select[name=zoom]').prop('value'));
        src+="&x="+xpos;
        src+="&y="+ypos;
        src+="&z="+zoom;
        $('#carte').prop('src',"/carte/image?"+src);
        $('#permalink').prop('href',"/carte/image?"+src);
    });
});

