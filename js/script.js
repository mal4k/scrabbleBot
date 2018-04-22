/**
 * Created by kamil on 16.03.2018.
 */
var board = [];
var hand = [];
var alphabet = "abcdefghijklmnopqrstuvwxyz";
function init_empty_hand(){
    for(var i = 0; i < 7; i++){
        hand.push(0)
    }
}
function init_empty_board(boardlength){

    for(var i = 0; i < boardlength; i++){
        board.push([]);
        $('#board').append('<tr id="board-row-' + i.toString() + '" class="board-row"></tr>');
        for(var j = 0; j < boardlength; j++){
            board[i].push(0);
            $('#board-row-' + i.toString()).append('<td id="field-' + i.toString() + '-' + j.toString() + '" class="field" ></td>')
        }
    }
    $('.field').each(function(){
        var id = $(this).attr('id');
        var parts = id.split("-");
        $(this).append('<input id="field-input-' + parts[1] + '-' + parts[2] + '" type="text" class="field-input" maxlength="1" align="center">')
    });

}
function add_special_field(){
    // add start field
    $('#field-7-7').addClass('start-field');
    // $('#field-7-7').append('<span>★</span>');


    // add triple word score
    $('#field-0-0').addClass('triple-word-score');
    $('#field-0-7').addClass('triple-word-score');
    $('#field-0-14').addClass('triple-word-score');
    $('#field-7-0').addClass('triple-word-score');
    $('#field-7-14').addClass('triple-word-score');
    $('#field-14-0').addClass('triple-word-score');
    $('#field-14-7').addClass('triple-word-score');
    $('#field-14-14').addClass('triple-word-score');

    // add double word score
    $('#field-1-1').addClass('double-word-score');
    $('#field-1-13').addClass('double-word-score');
    $('#field-2-2').addClass('double-word-score');
    $('#field-2-12').addClass('double-word-score');
    $('#field-3-3').addClass('double-word-score');
    $('#field-3-11').addClass('double-word-score');
    $('#field-4-4').addClass('double-word-score');
    $('#field-4-10').addClass('double-word-score');
    $('#field-10-4').addClass('double-word-score');
    $('#field-10-10').addClass('double-word-score');
    $('#field-11-3').addClass('double-word-score');
    $('#field-11-11').addClass('double-word-score');
    $('#field-12-2').addClass('double-word-score');
    $('#field-12-12').addClass('double-word-score');
    $('#field-13-1').addClass('double-word-score');
    $('#field-13-13').addClass('double-word-score');

    // add double letter score
    $('#field-0-3').addClass('double-letter-score');
    $('#field-0-11').addClass('double-letter-score');
    $('#field-2-6').addClass('double-letter-score');
    $('#field-2-8').addClass('double-letter-score');
    $('#field-3-0').addClass('double-letter-score');
    $('#field-3-7').addClass('double-letter-score');
    $('#field-3-14').addClass('double-letter-score');
    $('#field-6-2').addClass('double-letter-score');
    $('#field-6-6').addClass('double-letter-score');
    $('#field-6-8').addClass('double-letter-score');
    $('#field-6-12').addClass('double-letter-score');
    $('#field-7-3').addClass('double-letter-score');
    $('#field-7-11').addClass('double-letter-score');
    $('#field-8-2').addClass('double-letter-score');
    $('#field-8-6').addClass('double-letter-score');
    $('#field-8-8').addClass('double-letter-score');
    $('#field-8-12').addClass('double-letter-score');
    $('#field-11-0').addClass('double-letter-score');
    $('#field-11-7').addClass('double-letter-score');
    $('#field-11-14').addClass('double-letter-score');
    $('#field-12-6').addClass('double-letter-score');
    $('#field-12-8').addClass('double-letter-score');
    $('#field-14-3').addClass('double-letter-score');
    $('#field-14-11').addClass('double-letter-score');

    // add triple letter score
    $('#field-1-5').addClass('triple-letter-score');
    $('#field-1-9').addClass('triple-letter-score');
    $('#field-5-1').addClass('triple-letter-score');
    $('#field-5-5').addClass('triple-letter-score');
    $('#field-5-9').addClass('triple-letter-score');
    $('#field-5-13').addClass('triple-letter-score');
    $('#field-9-1').addClass('triple-letter-score');
    $('#field-9-5').addClass('triple-letter-score');
    $('#field-9-9').addClass('triple-letter-score');
    $('#field-9-13').addClass('triple-letter-score');
    $('#field-13-5').addClass('triple-letter-score');
    $('#field-13-9').addClass('triple-letter-score');

}
function read_board(){
    $('.field-input').each(function(){
       var char = $(this).val();
            var id = $(this).attr('id');
            var parts = id.split("-");
            var x = parseInt(parts[2]);
            var y = parseInt(parts[3]);
       if(char){
            board[x][y] = char;
       }
       else{
           board[x][y] = 0;
       }
    });
}
function read_hand(){
    $('.hand-input').each(function(){
        var char = $(this).val();
        if(char){
            var pos = $(this).attr('id').split("-")[3];
            hand[pos] = char;
        }
    })
}
function init_buttons(){
    $('#read-board-btn').on('click', function(){
       read_board();
    });
    $('#send-board-btn').on('click', function(){
        var data = prepare_data_for_send(board);
        data["do"] = "analyze";
        read_hand();
        data["hand"] = hand;
        data["duden"] = $('#check-duden').is(':checked');
        console.log($('#check-duden').is(':checked'));
        data["max-results"] = $('#max-results').val();
        $.ajax({
            type: 'POST',
            // url: "index.html",
            data: JSON.stringify(data)
        }).done(function(data){
            console.log(data)
        })
    });
    $('#test-board-btn').on('click', function(){
        init_test_board();
    });
    $('#clear-board-btn').on('click', function(){
        clear_board();
    });
    $('#test-hand-btn').on('click', function(){
        init_test_hand();
    })
}
function prepare_data_for_send(data){
    var result = {};
    for(var i = 0; i < data.length; i++){
        result["" + i] = data[i]
    }
    return result
}
function init_test_hand(){
    $('.hand-input').each(function(){
        var rand = Math.floor(Math.random() * (25));
        $(this).val(alphabet.charAt(rand))
    })
}
function init_test_board(){
    insert_word("troll", 7, 7);
    insert_word("kopfball", 6, 9, true)
}
function insert_word(word, x, y, vertical){
    vertical = (typeof vertical !== 'undefined') ? vertical : false;
    var i;
    if(vertical){
        for(i = 0; i < word.length; i++){
            insert_letter(word[i], x+i, y)        ;
        }
    }
    else{
        for(i = 0; i < word.length; i++){
            insert_letter(word[i], x, y+i);
        }
    }
}
function insert_letter(letter, x, y){
    $('#field-input-' + x + '-' + y).val(letter);
}
function clear_board(){
    $('.field-input').each(function () {
        $(this).val('');
    })
}
$(document).ready(function(){
    init_empty_hand();
    init_empty_board(15);
    add_special_field();
    init_buttons();
});
