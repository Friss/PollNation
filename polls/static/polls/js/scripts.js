/*-----------------------------------------------------------------------------------*/
/*	MENU
 /*-----------------------------------------------------------------------------------*/



/*-----------------------------------------------------------------------------------*/
/*	IMAGE HOVER
 /*-----------------------------------------------------------------------------------*/
$(document).ready(function () {
    $('.box').mouseenter(function (e) {

        $(this).children('a').children('span').fadeIn(200);
    }).mouseleave(function (e) {

            $(this).children('a').children('span').fadeOut(200);
        });
});

/*-----------------------------------------------------------------------------------*/
/*	HEADING
 /*-----------------------------------------------------------------------------------*/
(function ($) {

    $.fn.dcHeader = function (options) {

        var defaults = {
            padding: 0,
            onLoad: function () {
            },
            beforeLoad: function () {
            }
        };
        var options = $.extend(defaults, options);

        return this.each(function (options) {
            $(this).html('<span class="dchead left"></span><span class="dccontent">' + $(this).html() + '</span><span class="dchead right"></span><div class="clear"></div>');
            // onLoad callback;
            defaults.beforeLoad.call(this);
            $('span', this).css({display: 'block', textAlign: 'center'});
            $('.dchead.left, .dccontent').css({float: 'left'});
            $('.dchead.right').css({float: 'right'});
            var ht = $('.dccontent', this).height();
            var w = $(this).width();
            var wc = $('.dccontent', this).outerWidth(true) + (2 * defaults.padding);
            var wp = Math.round((w - wc) / 2);
            wc = w - (2 * wp);
            $('.dccontent', this).css({padding: 0, width: wc + 'px'});
            $('.dchead', this).css({padding: 0, height: ht + 'px', width: wp + 'px'});
            // onLoad callback;
            defaults.onLoad.call(this);
        });
    };
})(jQuery);


/*-----------------------------------------------------------------------------------*/
/*	MENU
 /*-----------------------------------------------------------------------------------*/
$(window).bind("load", function () {

    // Add to menu container
    $('.menu').dcHeader({
        padding: 15,
        beforeLoad: function () {

        }
    });

    // Add to header tags
    $('.line').dcHeader({padding: 10});

});


/*-----------------------------------------------------------------------------------*/
/*	TOGGLE
 /*-----------------------------------------------------------------------------------*/
$(document).ready(function () {
//Hide the tooglebox when page load
    $(".togglebox").hide();
//slide up and down when click over heading 2
    $("h2").click(function () {
// slide toggle effect set to slow you can set it to fast too.
        $(this).toggleClass("active").next(".togglebox").slideToggle("slow");
        return true;
    });
});


/*-----------------------------------------------------------------------------------*/
/*	TABS
 /*-----------------------------------------------------------------------------------*/
$(document).ready(function () {
    //Default Action
    $(".tab_content").hide(); //Hide all content
    $("ul.tabs li:first").addClass("active").show(); //Activate first tab
    $(".tab_content:first").show(); //Show first tab content

    //On Click Event
    $("ul.tabs li").click(function () {
        $("ul.tabs li").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tab_content").hide(); //Hide all tab content
        var activeTab = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
        $(activeTab).fadeIn(); //Fade in the active content
        return false;
    });

});

/*-----------------------------------------------------------------------------------*/
/*	PRETTYPHOTO
 /*-----------------------------------------------------------------------------------*/

$(document).ready(function () {
    $("a[rel^='prettyPhoto']").prettyPhoto({autoplay_slideshow: false, overlay_gallery: false, social_tools: false, deeplinking: false, theme: 'pp_default', slideshow: 5000});
});

/*-----------------------------------------------------------------------------------*/
/*	Multi-Choice input
 /*-------------------------------------------------------------------------------- */

$(document).ready(function () {

    // Code adapted from http://djangosnippets.org/snippets/1389/
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.item').remove();
            var forms = $('.item'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            var i = 0;
            // Go through the forms and set their indices, names and IDs
            for (formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).children().children().each(function () {
                    if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert("You have to enter at least one todo item!");
        }
        return false;
    }

    function addForm(btn, prefix) {

        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 10 todo items
        if (formCount < 10) {
            // Clone a form (without event handlers) from the first form
            var row = $(".item:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");
            $(row).children().find(":input").val('');

            // Relabel or rename all the relevant bits
            $(row).children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the delete item/form link
            $(row).find(".delete").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            alert("Sorry, you can only enter a maximum of ten items.");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "form");
    });

    $(".delete").click(function () {

        return deleteForm(this, "form");
    });
});