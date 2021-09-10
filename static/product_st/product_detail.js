// Cookie

function loadJson(selector) {
    return document.querySelector(selector).getAttribute('data-json');
}

function OnloadProductDetail() {
    const id = loadJson('#jsonData-id');
    console.log(id)
    $('#addToCartBtn').on('click', function () {
        alert('Successfully Added');
        $.post("http://127.0.0.1:8000/products/product_detail/" + id, $('#form').serialize(),
            function () {
                console.log($('#form').serialize());
            },
        )
    });
}


