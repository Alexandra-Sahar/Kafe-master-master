function dobavlenie_v_korzinu(tovar_id, kol_vo) {

    let tovari = localStorage.getItem('tovari');

    tovari = JSON.parse(tovari);

    if (tovari === null) {
        tovari = [{
            'id_tovara': tovar_id,
            'kol_vo': kol_vo
        }]

    }

    let naidenii_tovar = tovari.find(tovar => tovar.id_tovara === tovar_id);
    console.log(naidenii_tovar);
    if (naidenii_tovar === undefined) {
        tovari.push({
            'id_tovara': tovar_id,
            'kol_vo': kol_vo
        })
    }

    console.log(tovari);

    localStorage.setItem('tovari', JSON.stringify(tovari))

    $('.alert_bluda').show();
}


$(function () {
    $('.alert_bluda').hide();

    $('.btn_dobavlenie_v_korzinu').click(function (e) {
        e.preventDefault();
        let tovar_id = e.currentTarget.dataset['idBluda'];
        dobavlenie_v_korzinu(tovar_id, 1);
        $(e.currentTarget).text('Товар в корзине');
        $(e.currentTarget).toggleClass('btn-outline-success');
        $(e.currentTarget).toggleClass('btn-success');
    })
})