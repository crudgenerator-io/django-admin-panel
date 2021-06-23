/*global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
'use strict';
{
    function showAdminPopup(triggeringLink, name_regexp, add_popup) {
        const name = triggeringLink.id.replace(name_regexp, '');
        let href = triggeringLink.href;
        if (add_popup) {
            if (href.indexOf('?') === -1) {
                href += '?_popup=1';
            } else {
                href += '&_popup=1';
            }
        }
        const win = window.open(href, name, 'height=+screen.availHeight,width=+screen.availWidth,resizable=yes,scrollbars=yes');
        win.focus();
        return false;
    }

    function showRelatedObjectLookupPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^lookup_/, true);
    }

    function dismissRelatedLookupPopup(win, chosenId) {
        const name = win.name;
        const elem = document.getElementById(name);
        if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
            elem.value += ',' + chosenId;
        } else {
            document.getElementById(name).value = chosenId;
        }
        win.close();
    }

    function showRelatedObjectPopup(triggeringLink) {
        return showAdminPopup(triggeringLink, /^(change|add|delete)_/, false);
    }

    function updateRelatedObjectLinks(triggeringLink) {
        const $this = $(triggeringLink);
        const $dropdownMenu = $this.parent().parent().siblings('.related-widget-dropdown').find('.dropdown-menu');
        const $links = $dropdownMenu.children('.view-related, .change-related, .delete-related');
//        const siblings = $this.nextAll('.view-related, .change-related, .delete-related');
        if (!$links.length) {
            return;
        }
        const value = $this.val();
        if (value) {
            $dropdownMenu.find('.dropdown-divider, .dropdown-header').show();
            $links.show();
            $links.each(function() {
                const elm = $(this);
                elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
            });
        } else {
            $links.hide();
            $dropdownMenu.find('.dropdown-divider, .dropdown-header').hide();
            $links.removeAttr('href');
        }
    }

    function dismissAddRelatedObjectPopup(win, newId, newRepr) {
        let name = win.name;
        // odje win ima dodatno 'related_' iz nekog razlog todo debug
        name = name.replace('related__', '');
        const elem = document.getElementById(name);
        if (elem) {
            const elemName = elem.nodeName.toUpperCase();
            if (elemName === 'SELECT') {
                elem.options[elem.options.length] = new Option(newRepr, newId, true, true);
            } else if (elemName === 'INPUT') {
                if (elem.classList.contains('vManyToManyRawIdAdminField') && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                }
            }
            // Trigger a change event to update related links if required.
            $(elem).trigger('change');
            window.$(elem).selectpicker('refresh');
            window.$(elem).trigger('django:update-related');
        } else {
            const toId = name + "_to";
            const o = new Option(newRepr, newId);
            SelectBox.add_to_cache(toId, o);
            SelectBox.redisplay(toId);
        }
        win.close();
    }

    function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
        let id = win.name.replace(/^edit_/, '');
        // odje win ima dodatno 'related_' iz nekog razlog todo debug
        id = id.replace('related__', '');
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function() {
            if (this.value === objId) {
                this.textContent = newRepr;
                this.value = newId;
            }
        });
        window.$(selects).selectpicker('refresh'); // referenca na valjda malo noviji jquery sa kojim se selectpicker druzi well.
        win.close();
    }

    function dismissDeleteRelatedObjectPopup(win, objId) {
        const id = win.name.replace(/^delete_/, '');
        const selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
        const selects = $(selectsSelector);
        selects.find('option').each(function() {
            if (this.value === objId) {
                $(this).remove();
            }
        }).trigger('change');
        window.$(selects).selectpicker('refresh');
        win.close();
    }

    window.showRelatedObjectLookupPopup = showRelatedObjectLookupPopup;
    window.dismissRelatedLookupPopup = dismissRelatedLookupPopup;
    window.showRelatedObjectPopup = showRelatedObjectPopup;
    window.updateRelatedObjectLinks = updateRelatedObjectLinks;
    window.dismissAddRelatedObjectPopup = dismissAddRelatedObjectPopup;
    window.dismissChangeRelatedObjectPopup = dismissChangeRelatedObjectPopup;
    window.dismissDeleteRelatedObjectPopup = dismissDeleteRelatedObjectPopup;

    // Kept for backward compatibility
    window.showAddAnotherPopup = showRelatedObjectPopup;
    window.dismissAddAnotherPopup = dismissAddRelatedObjectPopup;

    $(document).ready(function() {
        $("a[data-popup-opener]").on('click', function(event) {
            event.preventDefault();
            opener.dismissRelatedLookupPopup(window, $(this).data("popup-opener"));
        });
        $('body').on('click', '.related-widget-wrapper-link', function(e) {
            e.preventDefault();
            if (this.href) {
                const event = $.Event('django:show-related', {href: this.href});
                $(this).trigger(event);
                if (!event.isDefaultPrevented()) {
                    showRelatedObjectPopup(this);
                }
            }
        });


        function handleSelectUpdate (select) {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                updateRelatedObjectLinks(select);
            }
        }

        $('body').on('change', '.related-widget-wrapper select', function(e) {
            handleSelectUpdate(this);
            // window.$(this).trigger('django:update-related');
        });

        // initial population of edit/delete links
        window.$('.related-widget-wrapper select').each((index, el) => {
            handleSelectUpdate(el);
        });

        $('body').on('click', '.related-lookup', function(e) {
            e.preventDefault();
            const event = $.Event('django:lookup-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                showRelatedObjectLookupPopup(this);
            }
        });
    });
}
