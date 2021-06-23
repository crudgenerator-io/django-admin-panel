const METADATA = {
    mapping: {
        qsFields: {
            sort: "order_by",
            page: "page",
            pageSize: "paginate_by",
            columns: "columns"
        },
        filterOperators: {
            contains: "contains",
            notContains: "!contains",
            exact: "exact",
            notExact: "!exact",
            lessThan: "lte",
            largerThan: "gte",
            equals: "equals",
            notEquals: "!equals",
            is: "is",
            isNot: "!is"
        },
        defaults: {
            boolean: {
                positive: "True",
                negative: "False"
            }
        },
        sortExpression: (field, direction) => {
            if(direction === "asc") {
                return "-" + field;
            } else {
                return field;
            }
        }
    },
    formats: {
        moment: {
            frontend: {
                // display formats (gijgo.js parsing)
                date: "YYYY-MM-DD",
                time: "HH:mm",
                datetime: "YYYY-MM-DD HH:mm"
            },
            backend: {
                // For default Django presentation format (moment.js parsing)
                date: "MMM. D, YYYY",
                time: "H:mm a",
                datetime: "MMM. D, YYYY, H:mm a"
            }
        },
        gijgo: {
            frontend: {
                // display formats (gijgo.js parsing)
                date: "yyyy-mm-dd",
                time: "HH:MM",
                datetime: "yyyy-mm-dd HH:MM"
            },
            backend: {
                // For default Django presentation format (moment.js parsing)
                date: "MMM. D, YYYY",
                time: "H:mm a",
                datetime: "MMM. D, YYYY, H:mm a"
            }
        }
    }
}


var createSnackbar = (function() {
    // Any snackbar that is already shown
    var previous = null;

    return function(message, actionText, action) {
        if (previous) {
            previous.dismiss();
        }
        var snackbar = document.createElement('div');
        snackbar.className = 'paper-snackbar';
        snackbar.dismiss = function() {
            this.style.opacity = 0;
        };
        var text = document.createTextNode(message);
        snackbar.appendChild(text);
        if (actionText) {
            if (!action) {
                action = snackbar.dismiss.bind(snackbar);
            }
            var actionButton = document.createElement('button');
            actionButton.className = 'action';
            actionButton.innerHTML = actionText;
            actionButton.addEventListener('click', action);
            snackbar.appendChild(actionButton);
        }

        if (!action) {
            setTimeout(function() {
                if (previous === this) {
                    previous.dismiss();
                }
            }.bind(snackbar), 5000);
        }


        snackbar.addEventListener('transitionend', function(event, elapsed) {
            if (event.propertyName === 'opacity' && this.style.opacity == 0) {
                this.parentElement.removeChild(this);
                if (previous === this) {
                    previous = null;
                }
            }
        }.bind(snackbar));

        previous = snackbar;

        if (window.screen.width <= 480) {
            document.body.appendChild(snackbar);
        } else {
            document.getElementsByClassName('main')[0].appendChild(snackbar);
        }

        getComputedStyle(snackbar).bottom;
        snackbar.style.bottom = '0px';
        snackbar.style.opacity = 1;
    };
})();

function create_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}


function getQuerystring(link, key) {
    var query = link.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == key) {
            return pair[1];
        }
    }
}

class TemplateManager {
    constructor($container) {
        this.$container = $container;
        this.templates = {};
        this.activeTemplate = null;
        this.init();
    }
    init () {
        for (let template of this.$container.children("template")) {
            this.templates[template.dataset.type] = {
                html: null,
                init: function () {
                },
                destroy: function () {
                }
            }
        }
    }
    activateTemplate (name, optionalParams = {}) {
        if (this.activeTemplate !== null) {
            this.templates[this.activeTemplate].html = null;
            this.$container.children().remove("*:not(template)");
        } else {
            if (this.templates[name].html === null) {
                this.templates[name].html = this.$container.find(`template[data-type=${name}]`)[0].content.cloneNode(true);
            }
        }
        this.activeTemplate = name;
        this.$container.append(this.templates[name].html);
        this.$container[0].setAttribute('data-active-template', this.activeTemplate);
        this.templates[name].init(optionalParams);
    }
    deactivateTemplate () {
        this.templates[this.activeTemplate].html = null;
        this.templates[this.activeTemplate].destroy();
        this.$container.children().remove("*:not(template)");
        this.activeTemplate = null;
    }
}


class ListingManager {
    $headingSelector = null;
    data = {};
    constructor() {
        // extract Backend data from dom (table element)
        const table = document.querySelector('table');
        if(!table) {
            return;
        }
        this.data['headers'] = Array.from(table.querySelectorAll('th'));
        this.data['data'] = Array.from(table.querySelectorAll('tbody tr')).map((row, i) => {
            return Array.from(row.querySelectorAll('td'))
        });
        table.remove();
    }
    getSelectedIds () {
        // To-be implemented in derived classes
    }
}

class TableManager extends ListingManager {
    constructor() {
        super();
        if(jQuery.isEmptyObject(this.data)) {
            return;
        }

        this.$table = $('<table class="table"></table>');

        const $tableHead = $('<thead></thead>');
        const $tableHeaders = $('<tr></tr>');
        $tableHeaders.append(`<th>
                <div class="material-checkbox">
                    <input type="checkbox" id="${this.data.headers[0].children[0].id}" name="${this.data.headers[0].children[0].name}">
                    <label for="${this.data.headers[0].children[0].id}"></label>
                </div>
            </th>`);
        for(let i=1;i<this.data.headers.length -1;i++) {
            const header = this.data.headers[i];
            if(header.classList.contains('sortable')) {
                header.children[0].classList.add('col-name');
                header.children[0].appendChild($(
                    `<div class="sort-icons-container">
                            <i class="material-icons clickable col-sort-icon">arrow_upward</i>
                            <i class="material-icons clickable col-sort-icon">arrow_downward</i>
                        </div>`
                )[0]);
            } else {
                header.innerHTML = `<span class="col-name">${header.textContent.trim()}</span>`;
            }
            $tableHeaders.append(header);
        }
        $tableHeaders.append('<th></th>');


        const $tableBody = $('<tbody></tbody>');
        this.data.data.forEach((tdList, i) => {
            const $tbodyRow = $('<tr></tr>');

            let checkboxAttrs = Array.from(tdList[0].children[0].attributes);
            let checkboxId = tdList[0].children[0].getAttribute('id');
            if(checkboxId === null) {
                checkboxId = {
                    name: 'id',
                    value: create_UUID()
                }
                checkboxAttrs.push(checkboxId);
            }
            checkboxAttrs = checkboxAttrs.map(x => `${x.name}="${x.value}"`).join(' ');
            $tbodyRow.append(`<td>
                <div class="material-checkbox">
                    <input ${checkboxAttrs}>
                    <label for="${checkboxId.value}"></label>
                </div>
            </td>`);

            for(let i=1;i<tdList.length - 1;i++) {
                const td = tdList[i];
                if (!td.classList.contains('checkmark-td')) {
                    td.innerHTML = `<span>${td.textContent.trim()}</span>`;
                } else {
                    if (td.classList.contains('positive')) {
                        td.innerHTML = `<i class="material-icons">check</i>`;
                    } else {
                        td.innerHTML = `<i class="material-icons">close</i>`;
                    }
                }

                $tbodyRow.append(td);
            }
            $tbodyRow.append(`<td>
                <div>
                    <a class="material-button" href="${tdList[tdList.length - 1].children[0].getAttribute('href')}"><i class="material-icons clickable" data-toggle="tooltip" title="Details" data-placement="bottom">arrow_forward</i></a> 
                </div>
            </td>`);
            $tableBody.append($tbodyRow);
        });


        this.$table.append($tableHead.append($tableHeaders));
        this.$table.append($tableBody);
        this.$table.appendTo(".card-body");

        this.$headers = this.$table.find("th:not(:first-child):not(:last-child)");
        this.$data = this.$table.find("td");

        this.tooltipOverflownTd();


        // setup event handlers
        // 1 - handler for row selection
        // 2 - for column sorting
        // 3 - manual triggering of a hover on th hover

        this.$table.find("th:first-child input[type='checkbox'], td:first-child input[type='checkbox']").on("change", (event) => {
            const isChecked = event.target.checked;
            const tableElement = event.target.parentElement.parentElement; // th or td
            let checkedNum = 0;
            if(tableElement.nodeName === "TD") {
                if(isChecked) {
                    tableElement.parentElement.classList.add("selected");
                } else {
                    tableElement.parentElement.classList.remove("selected");
                }
            } else {
                const tableDataRows = tableElement.parentElement.parentElement.parentElement.querySelectorAll("tbody tr");
                tableDataRows.forEach(function(tableRow) {
                    const tableRowCheckbox = tableRow.querySelector("input[type='checkbox']");
                    tableRowCheckbox.checked = isChecked;
                    if(isChecked) {
                        tableRow.classList.add('selected');
                    } else {
                        tableRow.classList.remove('selected');
                    }
                });
            }
            this.onCheck(tableElement.parentElement.parentElement.parentElement.querySelectorAll('tr.selected').length);
        });


        this.$headers.on("click", (event) => {
            const sortDirection = event.currentTarget.dataset.sortDirection;
            if(sortDirection !== undefined) {
                this.store.set(
                    METADATA.mapping.qsFields.sort,
                    METADATA.mapping.sortExpression(
                        event.currentTarget.dataset.fieldName,
                        event.currentTarget.dataset.sortDirection
                    ),
                    true
                )
            }
        });


        this.$headers.on('mouseover', (event) => {
            const x = $(event.currentTarget).find('a');
            x.hover();
        });

        this.$headers.on('click', (event) => {
            const x = $(event.currentTarget).find('a');
            x.click();
        });

        this.$headers.find('a').on('mouseover', function(e) {
            e.stopImmediatePropagation();
        });

        this.$headers.find('a').on('click', function(e) {
            e.stopPropagation();
        });

    }
    tooltipOverflownTd () {
        if (this.$headers) {
            this.$headers.each(function (i, th) {
                const span = th.querySelector(".col-name");
                if (span.scrollWidth > span.offsetWidth) {
                    let tooltipLeadingText = "", tooltipTrailingText = "";
                    if (th.dataset.sort !== undefined) {
                        tooltipLeadingText = "Sort by";
                        tooltipTrailingText = "ascending";
                        if (th.dataset.sort === "asc") {
                            tooltipTrailingText = "descending";
                        }
                    }

                    $(th).tooltip({
                        placement: "top",
                        trigger: "hover",
                        html: true,
                        title: tooltipLeadingText + " " + th.children[0].textContent + " " + tooltipTrailingText
                    });
                }

                const tdOrderingShift = 2 ; // css selectors begin at 1 + checkbox (1)
                const tds = $("td:nth-child(" + (tdOrderingShift + i) + ")");
                tds.each(function (y, td) {
                    if (td.scrollWidth > td.offsetWidth) {
                        const $td = $(td);
                        const $tdSpan = $td.children().first();
                        $td.tooltip({
                            placement: "bottom",
                            trigger: "manual",
                            title: $tdSpan.text(),
                        });
                        $tdSpan.on("mouseover", function () {
                            $td.tooltip("show");
                        });
                        $tdSpan.on("mouseleave", function () {
                            $td.tooltip("hide");
                        });
                    }
                });
            });
        }
    };
    getSelectedIds () {
        return this.$table.find("input[type='checkbox'][id*=row-selection]:checked").map((i, checkbox) => checkbox.id.replace("row-selection", ""));
    }

    onCheck(checkedNum) {
        // pass, implement anywhere to catch this event
    }
}

class CardsManager extends ListingManager {
    constructor() {
        super();

        if (this.data.data) {
            for(let data of this.data.data) {
                const $card = $(`
                <div class="card">
                    <div class="card-selection-backdrop">
                        <button class="material-button outlined card-selection-backdrop__btn">Unselect</button>
                    </div>
                </div>`
                );
                const $cardBody = $('<div class="card-body"></div>');

                $('<div class="record-header"></div>').append($(data[0].children[0])).appendTo($cardBody);
                for(let i=1;i<data.length - 1;i++) {
                    let content = data[i].textContent;
                    if (data[i].classList.contains('checkmark-td')) {
                        if (data[i].classList.contains('positive')) {
                            content = `<i class="material-icons">check</i>`;
                        } else {
                            content = `<i class="material-icons">close</i>`;
                        }
                    }
                    if(content !== '') {
                        $cardBody.append(`
                    <div class="record-field">
                        <div class="record-field__column">${this.data.headers[i].textContent}</div>
                        <div class="record-field__separator"><i class="material-icons">arrow_right_alt</i></div>
                    <div class="record-field__value">${content}</div>
                    </div>
                `);
                    }
                }
                $cardBody.append(`
                <div class="record-footer">
                    <i class="material-icons">subject</i>
                    <a class="record-footer__link material-button unobtrusive" href="${data[data.length - 1].children[0].getAttribute('href')}">DETAILS</a>
                </div>  
            `);
                $card.append($cardBody);
                $card.insertAfter('#mobile-paging-info-heading');
            }
        } else {
            $('<p id="no-records-text">No records found.</p>').insertAfter($('#mobile-paging-info-heading'));
        }


    }
}

class QueryStringManager {
    constructor() {
        this.qs = new URLSearchParams(window.location.search);
    }
    get (parameter) {
        return this.qs.get(parameter);
    }
    set (parameter, value, postUpdateReload=false) {
        if (value) {
            this.qs.set(parameter, value);
        } else {
            this.qs.delete(parameter);
        }
        if (postUpdateReload)  this.reload();
    }

    reload() {
        window.location.search = this.qs.toString();
    }
}

class FormManager {
    constructor(device) {

        // setup form validation
        this.$form = $('form');
        this.$form.validate({
            focusInvalid: false,
            errorPlacement: function ($error, $element) {
                const $fieldWrapper = $element.closest(".material-input, .material-select, .file-field");
                const $info = $fieldWrapper.find('.info');
                $info.data('original-info', $info.text());
                $info.text($error.text());
                $fieldWrapper.addClass("invalid");
            },
            success: function ($error, element) {
                const $element = $(element);
                const $filled = $element.closest(".material-input, .material-select, .file-field");
                const $info = $filled.find('.info');
                $info.text($info.data('original-info'));
                if (!$element.closest('div.field-' + $element.attr('name')).hasClass('errors')) {
                    // Don't assume it's valid bcs it's backend error
                    $filled.removeClass("invalid");
                }
            },
            invalidHandler: function (event, validator) {
                event.preventDefault();
                event.stopPropagation();
                const $inf = $('.management-tools__informational');
                $inf.addClass('error');
                $inf.empty();
                $inf.append($('<i class="material-icons">info</i><p class="errornote">Please correct the error below.</p>'));
            },
            onkeyup: function (element) {
                const $element = $(element);
                $(element).valid();
            }
        })


        // Materialize form elements
        $('input[type=text],  input[type=number],input[type=password],input[type=email]').each((index, el) => {
            if(Array.from(el.classList).some(cls => ['vDateField', 'vTimeField', 'vDateTimeField'].includes(cls))) return;

            const $el = $(el);

            let helpText = el.hasAttribute('required') ? '* Required' : 'Optional';
            const $helpTextEl = $el.siblings('.help');
            if ($helpTextEl.length > 0) {
                helpText += " - " + $helpTextEl.text();
                $helpTextEl.remove();
            }

            const maxlength = el.getAttribute('maxlength');
            const initialValueLength = el.value ? el.value.length : 0;
            $([
                el,
                $('<i class="material-icons error-icon">error</i>')[0],
                $('<span class="highlight"></span>')[0],
                $('<span class="bar"></span>')[0],
                $(`<span class="info">${helpText}</span>`)[0],
                $(`<span class="char-count">${maxlength ? (initialValueLength + "/" + maxlength) : ''}</span>`)[0],
                $(`label[for=${el.id}]`)[0],
            ]).wrapAll('<div class="material-input filled"></div>');

            if (maxlength) {
                $el.on('change keyup', () => {
                    const $charCount = $el.siblings(".char-count");
                    $charCount.text($el.val().length + "/" + $charCount.text().split("/")[1]);
                });
            }

            if (el.type === 'number') {
                // Ignore letter 'e'
                $el.on("keypress", function (event) {
                    if (event.which === 101) {
                        event.preventDefault();
                    }
                });
            }

            if (el.value !== '') el.parentElement.classList.add('has-value');
            $el.on('keyup change', (event) => {
                if (el.value.trim() !== '') {
                    el.parentElement.classList.add('has-value')
                } else {
                    el.parentElement.classList.remove('has-value');
                }
            });
            if ($helpTextEl.length > 0) el.parentElement.classList.add('has-helptext');

            const $errors = $el.closest('div[class*=field-]').find('ul.errorlist li');
            const hasErrors = $errors.length > 0;
            const $materialInputWrap = $el.closest('.material-input');
            if (hasErrors) {
                $materialInputWrap.addClass('invalid');
                const errorText = Array.from($el.closest('div[class*=field-]').find('ul.errorlist li').map((index, el) => el.textContent)).join(', ');
                $errors.parent().hide();
                $el.siblings('.info').text(errorText);
            }
        });

        $('textarea').each((index, el) => {
            const $el = $(el);

            let helpText = el.hasAttribute('required') ? '* Required' : 'Optional';
            const $helpTextEl = $el.siblings('.help');
            if ($helpTextEl.length > 0) {
                helpText += " - " + $helpTextEl.text();
                $helpTextEl.remove();
            }

            $([
                el,
                $('<i class="material-icons error-icon">error</i>')[0],
                $('<span class="highlight"></span>')[0],
                $('<span class="bar"></span>')[0],
                $(`<span class="info">${helpText}</span>`)[0],
                $(`<span class="char-count">${el.hasAttribute('maxlength') ? "0/" + el.getAttribute('maxlength') : ''}</span>`)[0],
                $(`label[for=${el.id}]`)[0],
            ]).wrapAll('<div class="material-input filled"></div>');


            if (el.textContent) el.parentElement.classList.add('has-value');
        });

        $('input[type=checkbox]').each((index, el) => {
            if (el.attributes.hidden) {
                // No need to 'materialize' checkboxes which are hidden from interface (example - django file remove checkbox)
                return;
            }

            const $el = $(el);

            const $help = $el.siblings('.help');
            if ($help.length) {
                const $helpIcon = $('<i class="material-icons help-icon" data-toggle="tooltip" data-placement="top" title="' + $help.text() + '">help</i>');
                $helpIcon.insertAfter($help);
                $help.remove();
            }

            $([
                el,
                $(`label[for=${el.id}]`)[0],
            ]).wrapAll('<div class="material-checkbox">');
        });

        $("input[type=file]").each((index, el) => {
            const $el = $(el);
            const $help = $el.siblings('.help');

            const clearCheckbox = $el.siblings('input[type=checkbox]')[0];
            const isRequired = el.hasAttribute('required') || $el.siblings('label').hasClass('required');
            if (isRequired && el.getAttribute('required') === null) {
                el.setAttribute('required', '');
            }

            $([
                $(`label[for=${el.id}]`)[0],
                el,
                clearCheckbox
            ]).wrapAll(`<div class="file-field ${isRequired ? 'is-required' : ''}">`);


            const $errors = $el.closest('div[class*=field-]').find('ul.errorlist li');
            const hasErrors = $errors.length > 0;
            const $fileFieldWrap = $el.closest('.file-field');
            let infoText = "";
            if (hasErrors) {
                $fileFieldWrap.addClass('invalid');
                infoText = Array.from($el.closest('div[class*=field-]').find('ul.errorlist li').map((index, el) => el.textContent)).join(', ');
                $errors.parent().hide();
                $help.hide();
            } else {
                if (isRequired) {
                    infoText = '* Required';
                } else {
                    infoText = 'Optional';
                }
                if ($help.length) {
                    infoText += " - " + $help.text();
                    $help.hide();
                }
            }
            $fileFieldWrap.append($(`<div class="info">${infoText}</div>`));

            if (clearCheckbox) {
                $el.MDFiles({
                    onDelete: function () {
                        clearCheckbox.checked = true;
                        if (isRequired) {
                            $fileFieldWrap.addClass('invalid');
                            $fileFieldWrap.find('.info').text(isRequired ? 'This field is required': 'There was an error trying to remove the file');
                        }
                    },
                    onAdd: function () {
                        clearCheckbox.checked = false;
                        if (hasErrors) {
                            $fileFieldWrap.removeClass('invalid');
                            $fileFieldWrap.find('.info').text(isRequired ? '* Required': '');
                        }
                    }
                });
            } else {
                $el.MDFiles(
                    {
                        onDelete: function () {
                            clearCheckbox.checked = true;
                        },
                        onAdd: function () {
                            if (hasErrors) {
                                $fileFieldWrap.removeClass('invalid');
                                $fileFieldWrap.find('.info').text(isRequired ? '* Required': '');
                            }
                        }
                    }
                );
            }
        });

        $('input[class=vDateField], input[class=vTimeField], input[class=vDateTimeField]').each((index, el) => {
            const $el = $(el);

            let helpText = el.hasAttribute('required') ? '* Required' : 'Optional';
            const $helpTextEl = $el.siblings('.help');
            if ($helpTextEl.length > 0) {
                helpText += " - " + $helpTextEl.text();
                $helpTextEl.remove();
            }

            $([
                el,
                $('<i class="material-icons error-icon">error</i>')[0],
                $('<span class="highlight"></span>')[0],
                $('<span class="bar"></span>')[0],
                $(`<span class="info">${helpText}</span>`)[0],
                $(`<span class="char-count">${el.hasAttribute('maxlength') ? "0/" + el.getAttribute('maxlength') : ''}</span>`)[0],
                $(`label[for=${el.id}]`)[0],
            ]).wrapAll('<div class="material-input filled leading-icon" role="wrapper">');


            let val = null;
            if ($el.hasClass('vDateField')) {
                val = $el.attr('value');
                $el.removeAttr('value');


                function initialValueIsValid () {
                    return val !== undefined && val !== '' && val !== 'None';
                }
                $el.datepicker({
                    format: METADATA.formats.gijgo.frontend.date,
                    icons: {
                        rightIcon: '<i class="material-icons clickable">today</i>',
                        previousMonth: '<i class="material-icons clickable">keyboard_arrow_left</i>',
                        nextMonth: '<i class="material-icons clickable">keyboard_arrow_right</i>'
                    },
                    modal: device === 'mobile',
                    footer: device === 'mobile',
                    showOnFocus: false,
                    change: function (evt) {
                        $(this).valid();
                    },
                    value: initialValueIsValid() ? (moment(val, METADATA.formats.moment.backend.date).format(METADATA.formats.moment.frontend.date)) : null
                });
            } else if ($el.hasClass('vTimeField')) {
                val = $el.attr('value');
                $el.removeAttr('value');

                function initialValueIsValid () {
                    return val !== undefined && val !== '' && val !== 'None';
                }

                $el.timepicker({
                    format: METADATA.formats.gijgo.frontend.time,
                    icons: {
                        rightIcon: '<i class="material-icons clickable">schedule</i>'
                    },
                    showOnFocus: false,
                    modal: device === 'mobile',
                    footer: true,
                    change: function (evt) {
                        $(this).valid();
                    },
                    value: initialValueIsValid() ? (moment(val, METADATA.formats.moment.backend.time).format(METADATA.formats.moment.frontend.time)) : null
                });


            } else {
                const $dateInput  = $el.parent().prev().find('[type=date]');
                const $timeInput = $el.parent().prev().find('[type=time]');

                const initialVal = moment($dateInput.val() + ' ' + $timeInput.val());
                $el.datetimepicker({
                    icons: {
                        rightIcon: '<i class="material-icons clickable">today</i>',
                        previousMonth: '<i class="material-icons clickable">keyboard_arrow_left</i>',
                        nextMonth: '<i class="material-icons clickable">keyboard_arrow_right</i>'
                    },
                    format: METADATA.formats.gijgo.frontend.datetime,
                    showOnFocus: false,
                    change: function (evt) {
                        $(this).valid();
                    },
                    modal: device === 'mobile',
                    footer: true,
                    value: initialVal.isValid() ? initialVal.format(METADATA.formats.moment.frontend.datetime) : null
                });

                $el.on('change', () => {
                    const newVal = moment($el.val());
                    $dateInput.val(newVal.format('YYYY-MM-DD'));
                    $timeInput.val(newVal.format('HH:mm'));
                });

            }
            if ($el.val()) {
                $el.parent().addClass('has-value');
            }
            $el.on('change', () => {
                if (el.value !== '') {
                    el.parentElement.classList.add('has-value')
                } else {
                    el.parentElement.classList.remove('has-value');
                }
            });


            const $mdInput = $el.closest('.material-input');
            const $errorlist = $mdInput.siblings('.errorlist');
            if ($errorlist.children().length) {
                const errorText = Array.from($errorlist.children().map((index, li) => li.textContent)).join("\n");
                const $info = $mdInput.find('.info');
                $info.data('original-info', $info.text());
                $info.text(errorText);
                $errorlist.hide();
            }
        });

        $('select').each((index, el) => {
            const $el = $(el);


            // Django formsets
            const $formsetWrapper = $el.closest('.js-inline-admin-formset');
            if ($formsetWrapper.length) {
                // Setup for stacked inline relationships (backrefed)
                let $connectionsFieldset = $('form fieldset .name:contains(Connections)').parent();
                if (!$connectionsFieldset.length) {
                    $connectionsFieldset = $('<fieldset class="module"><div class="name">Connections</div></fieldset>');
                    $('form').append($connectionsFieldset);
                }

                // Create pivoting select (which acts as a manager)
                if ($formsetWrapper.hasClass('done-setup')) {
                    // It's already done setuping - just gather the values from exising select
                    if ($el.val()) {
                        const $pivotSel = $formsetWrapper.find('select[id*=__pivot__]');
                        $pivotSel.find(`option[value=${$el.val()}]`)[0].setAttribute('selected', '');
                        $pivotSel.selectpicker('refresh');
                    }
                    return;
                }

                const wrap = $formsetWrapper.wrap(`<div class="field-${$formsetWrapper.attr('id')}"></div>`).parent();
                wrap.appendTo($connectionsFieldset);
                const $widgetDropdown = $('.inline-related.empty-form .related-widget-dropdown');
                $widgetDropdown.appendTo($formsetWrapper);
                $widgetDropdown.find('.dropdown-menu').children('*:not(.add-related)').remove();


                const selId = $formsetWrapper.data('inline-formset').options.prefix + "-__pivot__";
                // So that popup would work properly
                $widgetDropdown.find('a').attr('id', `add_related__${selId}`);

                const selOptions = $el.find('option').clone();

                const $sel = $(`<select id="${selId}" multiple></select>`);
                $sel.append(selOptions);
                // remove unnecessary first option - - - - - - - - (comes with blank=True)
                $sel[0].options[0].remove();
                $formsetWrapper.append($sel);

                let labelText = $formsetWrapper.find('fieldset[class*=relationship_verbose_name]').attr('class').split('relationship_verbose_name__')[1];
                labelText = labelText.charAt(0).toUpperCase() + labelText.slice(1);
                $formsetWrapper.append($(`<label for="${$sel[0].id}">${labelText}</label>`));

                $([
                    $sel[0],
                    $('<span class="highlight"></span>')[0],
                    $('<span class="bar"></span>')[0],
                    $(`<span class="info">Optional</span>`)[0],
                    $(`label[for=${$sel[0].id}]`)[0],
                ]).wrapAll(`<div class="material-select filled has-value has-dropdown"></div>`);

                let liveSearch = false;
                const optionsCount = $el.children().length;
                if (optionsCount > 0) {
                    if (optionsCount > 5) {
                        liveSearch = true;
                    }
                }

                const isMobile = device === 'mobile';

                $sel.selectpicker({
                    liveSearch: liveSearch,
                    liveSearchPlaceholder: 'Search ..',
                    selectedTextFormat: 'count > 1',
                    showTick: !isMobile,
                    footerButtons: isMobile,
                    multiple: true
                });


                $sel.on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
                    const optionValue = e.target.options[clickedIndex].value;
                    const $targetSel = $formsetWrapper.find('select:not([id*=__pivot__])').filter((index, el) => el.value == optionValue);
                    const $targetSelDeleteCheckbox = $targetSel.closest('.inline-related').find('.delete input[type=checkbox]');
                    if (isSelected) {
                        // if relationship already exist means delete has been checked - just uncheck it
                        // in other case - handle adding another relationship

                        if ($targetSel.length) {
                            $targetSelDeleteCheckbox[0].checked = false;
                        } else {
                            $(document).on('formset:added', function(e, newRelSelect) {
                                $(newRelSelect).find('option[value='+ optionValue +']')[0].setAttribute('selected', '');
                            });
                            $formsetWrapper.find('.add-row > a')[0].click();
                            $(document).off('formset:added');
                        }
                    } else {
                        // if it's newly added there's no checkbox - trigger removal of whole formset
                        if (!$targetSelDeleteCheckbox.length) {
                            $targetSel.closest('.inline-related').find('.inline-deletelink')[0].click();
                        } else {
                            // in other case - just uncheck
                            $targetSelDeleteCheckbox[0].checked = true;
                        }
                    }
                });

                $sel.on('django:update-related', function() {
                    // As it's only add operation supported supported
                    $(document).on('formset:added', function(e, relInlineRelated) {
                        const $opt = $sel.find('option:last');
                        const $relSelect = relInlineRelated.find('select');
                        $relSelect.append($opt.clone());
                        $opt[0].setAttribute('selected', '');
                    });
                    $formsetWrapper.find('.add-row > a')[0].click();
                    $(document).off('formset:added');
                });


                if (isMobile) {
                    el.parentElement.parentElement.classList.add('custom-mobile-select');
                    $sel.on('shown.bs.select', function() {
                        $('[data-toggle=tooltip]').tooltip('hide');
                    });
                }

                $formsetWrapper.addClass('done-setup');
            } else {
                // Django doesn't include required attribute in required selects, so opting to extract that info from corresponding label (which does hold required class)
                if ($el.siblings('label').hasClass('required')) {
                    $el.prop('required', true);
                }

                let helpText = el.hasAttribute('required') ? '* Required' : 'Optional';
                const $helpTextEl = $el.siblings('.help');
                if ($helpTextEl.length > 0) {
                    helpText += " - " + $helpTextEl.text();
                    $helpTextEl.remove();
                }

                let isInvalid = false;
                if ($el.siblings('.errorlist').children().length) {
                    isInvalid = true;
                }

                $([
                    el,
                    $('<span class="highlight"></span>')[0],
                    $('<span class="bar"></span>')[0],
                    $(`<span class="info">${helpText}</span>`)[0],
                    $(`label[for=${el.id}]`)[0],
                ]).wrapAll(`<div class="material-select filled ${el.hasAttribute('required') ? 'is-required' : ''} has-value ${isInvalid ? 'invalid': ''}"></div>`);

                let liveSearch = false, actionsBox = false;
                const optionsCount = $el.children().length;
                if (optionsCount > 0) {
                    actionsBox = true;
                    if (optionsCount > 5) {
                        liveSearch = true;
                    }
                }

                const isMobile = device === 'mobile';

                const $sel = $el.selectpicker({
                    liveSearch: liveSearch,
                    liveSearchPlaceholder: 'Search ..',
                    actionsBox: actionsBox,
                    selectedTextFormat: 'count > 1',
                    showTick: !isMobile,
                    footerButtons: isMobile
                });

                if (isMobile) {
                    el.parentElement.parentElement.classList.add('custom-mobile-select');
                    $sel.on('shown.bs.select', function() {
                        $('[data-toggle=tooltip]').tooltip('hide');
                    });
                }

                const $relFieldWrapper = $el.closest('.material-select');
                const $errorlist = $relFieldWrapper.siblings('.errorlist');
                if (isInvalid) {
                    const errorText = Array.from($errorlist.children().map((index, li) => li.textContent)).join("\n");
                    const $info = $relFieldWrapper.find('.info');
                    $info.data('original-info', $info.text());
                    $info.text(errorText);
                    $errorlist.hide();
                }
            }
        });

        // Remove colons from labels
        const $labels = $('label');
        $labels.each((index, label) => {
            label.textContent = label.textContent.replace(':', '');
        });


        // Fieldset distribution (wrap at 3)
        const $fieldsets = $('form > fieldset');
        const $fD = $('<div class="filler"></div>'), $sD = $('<div class="filler"></div>'),
            $tD = $('<div class="filler"></div>');
        $fieldsets.each((index, fieldset) => {
            if (index % 3 === 0) $fD.append($(fieldset));
            else if (index % 3 === 1) $sD.append($(fieldset));
            else $tD.append($(fieldset));
        });

        const $submitRow = $('.submit-row');

        $submitRow.find('input[name=_addanother], input[name=_continue]').addClass(`material-button text`);
        $submitRow.find('input[name=_save]').addClass(`material-button contained`);
        const $submitRowDeleteLink = $submitRow.find('a.deletelink');

        const $managementTools = $('<div id="management-tools"></div>');
        const $managementRow = $('<div id="management-row"></div>');
        const $objTools = $('.object-tools');
        const objectToolsLinks = []
        $objTools.children().each((index, link) => {
            const a = $(link).find('a')[0];
            objectToolsLinks.push([a.getAttribute('href'), a.textContent]);
        });
        $objTools.hide();


        if ($submitRowDeleteLink.length !== 0) {
            $submitRowDeleteLink.hide();
            objectToolsLinks.push([$submitRowDeleteLink[0].getAttribute('href'), $submitRowDeleteLink[0].textContent]);
        }

        if(objectToolsLinks.length > 0) {
            const iconText = device === 'mobile' ? 'more_vert' : 'more_horiz';
            $managementTools.append($(
                `<div class="dropdown">
                <i class="material-icons clickable" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">${iconText}</i>
                    <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        ${objectToolsLinks.map(tool => `<a href="${tool[0]}" class="dropdown-item">${tool[1]}</a>`).join('')}
                    </div>
                </div>`
            ));
            $managementRow.append($managementTools)
        }

        if (!$fieldsets.length) {
            // If class doesn't have atleast 1 field/relationship
            $('form').append('<p>No editable fields for this entity</p>');
        }

        const $formP = $('form > p');


        const $informational = $('<div class="management-tools__informational"></div>');
        $informational.appendTo($managementTools);

        if($formP.length) {
            const generalErrors = $formP.filter((index, el) => el.classList.contains('errornote'));
            $('<i class="material-icons">info</i>').appendTo($informational);
            if (generalErrors.length === 0) {
                $formP.appendTo($informational);
            } else {
                $informational.addClass('error');
                generalErrors.appendTo($informational);
                $formP.not(generalErrors).hide();
            }
        }


        $managementRow.append($managementTools);
        $submitRow.find('.deletelink-box').remove();
        $managementRow.append($submitRow);

        if(device === 'mobile') {
            const $mobileActionsContainer = $('#top-navbar-lower__mobile-actions-container');
            $managementRow.find('.dropdown').appendTo($mobileActionsContainer);
            $managementRow.hide();
            $mobileActionsContainer.append(`<i class="material-icons" onclick="document.querySelector('input[name=_save]').click()">send</i>`)
        }


        const $form = $('form');
        $form.append($managementRow);
        $form.append($fD);
        $form.append($sD);
        $form.append($tD);



        // Django uses 'related-widget-wrapper' in their js for relationships
        $('.material-select').addClass('related-widget-wrapper');
        const $relatedWidgetWrappers = $('.related-widget-wrapper');
        $relatedWidgetWrappers.each((index, el) => {
            const $el = $(el);
            if ($el.next('.related-widget-dropdown').length > 0) {
                $el.addClass('has-dropdown');
            }
        });
    }
}

class Page {
    constructor() {
        this.device = (() => {

            // Device based rendering based on hardware detection
            // if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
            //
            // }


            // Device based rendering based on screen size detection
            if (window.innerWidth <= 480) {
                return "mobile";
            } else {
                return "desktop";
            }
        })()
    }
    setup() {
        const device = this.device;

        $("#mobile-navigation-close").on("click", function () {
            const $sidebar = $(".sidebar").first();
            $sidebar.removeClass("extended");
        });
        $("#navigation-drawer-btn").on("click", function (e) {
            const $sideNavbar = $("#side-navbar").first();
            if ($sideNavbar.hasClass("extended")) {
                if (device !== 'mobile') {
                    $('body').removeClass('nav-extended');
                }

                $sideNavbar.removeClass("extended");
            } else {
                if (device !== 'mobile') {
                    $('body').addClass('nav-extended');
                }

                $sideNavbar.addClass("extended");
            }
        });
        $('#side-navbar__backdrop').on('click', () => {
            $('body').removeClass('nav-extended');
            $("#side-navbar").removeClass("extended");
        });

        // Init all tooltips
        const $tooltips = $('[data-toggle="tooltip"]').tooltip({
            container: "body",
            trigger: device === 'mobile' ? 'click': 'hover'
        });
        if (device === 'mobile') {
            $(document).on('click', function(event) {
                if (event.target.dataset.toggle) {
                    hideTooltips(event.target);
                } else {
                    hideTooltips();
                }
            });
        }

        function hideTooltips (exemptEl) {
            $tooltips.not($(exemptEl)).tooltip('hide');
        }


        // Notification message snackbar
        const notificationMessageContent = $('.notification-message > span').text();
        if (notificationMessageContent) {
            createSnackbar(notificationMessageContent);
        }
    }

    rendered () {
        // code to exec after completed rendering and content shown
    }
}

$(document).ready(function () {
    const pageType = document.querySelector(".main").dataset.pageType;
    let page;

    function pageAvailable (pageName, callBackFn) {
        const interval = 10;
        setTimeout(function() {
            if (window[pageName]) {
                callBackFn(window[pageName]);
            }  else {
                pageAvailable(pageName, callBackFn);
            }
        });
    }

    pageAvailable(pageType.split('-').map(x => x.charAt(0).toUpperCase() + x.slice(1)).join("") + 'Page', function() {
        if (pageType === "list") {
            page = new ListPage();
        } else if (pageType === "form") {
            page = new FormPage();
        } else if (pageType === 'history') {
            page = new HistoryPage();
        } else if (pageType === 'delete') {
            page = new DeletePage();
        } else if (pageType === 'full-page-form') {
            page = new FullPageFormPage();
        } else if (pageType === 'index') {
            page = new IndexPage();
        } else {
            page = new Page();
        }
        page.setup();

        if(page.device !== 'mobile') {
            $('#navigation-drawer-btn').trigger('click');
        } else {
            const $main = $('.main');
            if ($main.hasClass('has-filters')) {
                $('.sidebar-action-btn[data-type=applied-filters-mobile]').trigger('click');
            }
            // Store theme color
            $(document).data('original-theme-color', $('meta[name=theme-color]').attr('content'));
        }

        document.body.style.display = 'initial';

        page.rendered();
    });
});


const $document = $(document);
const MEDIA_SRC = "/assets";