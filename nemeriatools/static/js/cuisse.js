$(function() {
    var table=$('#troupetable');
    var totaux=[];
    var entrees=[];
    $('.btn[name=add1]').click(function() { addunits(1);});
    $('.btn[name=add2]').click(function() { addunits(2);});
    $('.btn[name=add3]').click(function() { addunits(3);});
    $('.input[type=text]').change(function() { update() });
    addunits=function(type, total) {
        var row=$('<tr></tr>');
        for (i=1;i<=8;i++) {
            if (total==true) { row.append('<td><div class="total troupes p'+type+' u'+i+'"></div><input type="text" class="input-mini" disabled="disabled"></td>') }
            else { row.append('<td><div class="troupes p'+type+' u'+i+'"></div><input type="text" class="input-mini"></td>') }
        }
        table.append(row);
    }
    update=function() {
        $('.troupes').each(function() {
            if ($(this).prop("class").indexOf("total") != -1) {
                // contient total, alors on met 0 dedans
                $(this).siblings('.input-mini').prop("value",0);
            }
            else {
                classe=$(this).prop('class').match(/p\d/)[0];
                unit=$(this).prop('class').match(/u\d/)[0];
                nombre=parseInt($('div.'+classe+';div.'+unit+';div.total').siblings('input').prop('value'));
                if (!($(this).siblings('input').prop('value').match(/\d+/))) {
                    $(this).siblings('input').prop('value',0);
                }
                nombre+=parseInt($(this).siblings('input').prop('value'));
                $('div.'+classe+';div.'+unit+';div.total').siblings('input').prop('value',nombre);
            }
        });
    }
    addunits(1,true);
    addunits(2,true);
    addunits(3,true);
});
