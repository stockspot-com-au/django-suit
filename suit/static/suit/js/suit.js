(function ($) {

    // Register callbacks to perform after inline has been added
    Suit.after_inline = function () {
        var functions = {};
        var register = function (fn_name, fn_callback) {
            functions[fn_name] = fn_callback;
        };

        var run = function (inline_prefix, row) {
            for (var fn_name in functions) {
                functions[fn_name](inline_prefix, row);
            }
        };

        return {
            register: register,
            run: run
        };
    }();

    // Backwards compatiblity
    window.SuitAfterInline = Suit.after_inline;

    // Django's inlines.js dispatches "formset:added" for every added form
    document.addEventListener('formset:added', function (e) {
        var prefix = e.detail && e.detail.formsetName;
        Suit.after_inline.run(prefix, $(e.target));
    });

    /**
     * Fixed submit buttons. Kept for backwards compatibility: the right
     * column is now position: sticky in suit.css.
     */
    $.fn.suit_fixed = function () {
        return this;
    };


    /**
     * Search filters - submit only changed fields
     */
    $.fn.suit_search_filters = function () {
        $(this).on('change', function () {
            var $field = $(this);
            var $option = $field.find('option:selected');
            var select_name = $option.data('name');
            if (select_name) {
                $field.attr('name', select_name);
            } else {
                $field.removeAttr('name');
            }
            // Handle additional values for date filters
            var additional = $option.data('additional');
            if (additional) {
                var hidden_id = $field.data('name') + '_add';
                var $hidden = $('#' + hidden_id);
                if (!$hidden.length) {
                    $hidden = $('<input/>').attr('type', 'hidden').attr('id', hidden_id);
                    $field.after($hidden);
                }
                additional = additional.split('=');
                $hidden.attr('name', additional[0]).val(additional[1]);
            }
        });
        $(this).trigger('change');
    };

    /**
     * Linked select - shows link to related item after Select
     */
    $.fn.suit_linked_select = function () {

        var get_link_name = function ($select) {
            var text = $select.find('option:selected').text();
            return text && $select.val() ? text + '' : '';
        };

        var get_url = function ($select) {
            var value = $select.val();
            if (!value) {
                return null;
            }
            // Django's related widget wrapper knows the change url of the selected object
            var $change = $select.closest('.related-widget-wrapper').find('a.change-related, a.view-related').first();
            var template = $change.data('href-template');
            if (template) {
                return template.replace('__fk__', encodeURIComponent(value)).replace(/[?&]_popup=1/, '');
            }
            var $add = $select.siblings('a.add-related, a.add-another').first();
            if ($add.length) {
                return $add.attr('href').split('?')[0] + '../' + encodeURIComponent(value) + '/change/';
            }
            return null;
        };

        var add_link = function ($select) {
            var $container = $select.closest('.related-widget-wrapper');
            if (!$container.length) {
                $container = $select.parent();
            }
            var $link = $container.find('a.linked-select-link');
            if (!$link.length) {
                $link = $('<a/>').addClass('linked-select-link');
                $container.append($link);
            }
            var url = get_url($select);
            $link.text(url ? get_link_name($select) : '');
            if (url) {
                $link.attr('href', url);
            } else {
                $link.removeAttr('href');
            }
        };

        $(this).each(function () {
            add_link($(this));
        });

        $(document).on('change', 'select.linked-select', function () {
            add_link($(this));
        });
    };

    /**
     * Content tabs
     */
    $.fn.suit_form_tabs = function () {

        var $tabs = $(this);
        var tab_prefix = $tabs.data('tab-prefix');
        if (!tab_prefix)
            return;

        var $tab_links = $tabs.find('a');

        function tab_contents($link) {
            return $('.' + tab_prefix + '-' + $link.attr('href').replace('#', ''));
        }

        function activate_tabs() {
            // Init tab by error, by url hash or init first tab
            var found_error = false;
            $tab_links.each(function () {
                var $link = $(this);
                if (tab_contents($link).find('.errors, .errorlist').length) {
                    $link.addClass('error');
                    if (!found_error) {
                        $link.trigger('click');
                        found_error = true;
                    }
                }
            });
            if (found_error) {
                return;
            }
            var $hash_link = window.location.hash ? $tab_links.filter(function () {
                return $(this).attr('href') === window.location.hash;
            }) : $();
            ($hash_link.length ? $hash_link : $tab_links.first()).trigger('click');
        }

        $tab_links.on('click', function (e) {
            var $link = $(this);
            e.preventDefault();
            $tab_links.removeClass('active').removeAttr('aria-current');
            $link.addClass('active').attr('aria-current', 'page');
            $('.' + tab_prefix).removeClass('show');
            tab_contents($link).addClass('show');
            if (window.history && window.history.replaceState) {
                window.history.replaceState(null, '', $link.attr('href'));
            }
        });

        activate_tabs();
    };

    /**
     * Avoids double-submit issues in the change_form.
     */
    $.fn.suit_form_debounce = function () {
        var $form = $(this),
            $saveButtons = $form.find('.submit-row button, .submit-row input[type=submit]'),
            submitting = false;

        $form.on('submit', function () {
            if (submitting) {
                return false;
            }

            submitting = true;
            $saveButtons.addClass('disabled');

            setTimeout(function () {
                $saveButtons.removeClass('disabled');
                submitting = false;
            }, 5000);
        });
    };

    /**
     * Autosize textareas - grow with content. Browsers supporting
     * "field-sizing: content" do it with CSS only.
     */
    var supports_field_sizing = window.CSS && CSS.supports && CSS.supports('field-sizing', 'content');

    function autosize(el) {
        if (supports_field_sizing || !el || el.tagName !== 'TEXTAREA') {
            return;
        }
        el.style.height = 'auto';
        el.style.height = (el.scrollHeight + el.offsetHeight - el.clientHeight) + 'px';
    }

    $.fn.autosize = function () {
        return this.each(function () {
            autosize(this);
        });
    };

    $(document).on('input', 'textarea.autosize', function () {
        autosize(this);
    });

    Suit.after_inline.register('autosize', function (prefix, row) {
        $(row).find('textarea.autosize').autosize();
    });

    $(function () {

        // Show link to related item after Select
        $('.linked-select').suit_linked_select();

        // Handle change list filter null values
        $('.search-filter').suit_search_filters();

        $('textarea.autosize').autosize();

    });

}(Suit.$));
