// Add 'table' class to table tag in post_detail.html.
// the table is generated dynamically from the markdown code.
// For this reason, the class is added using javascript
document.addEventListener('DOMContentLoaded', function() {
    var tables = document.getElementsByTagName('table');
    for (var i = 0; i < tables.length; i++) {
        tables[i].classList.add('table');
    }
});