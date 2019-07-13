//Hier wird die Food to Fork api abgerufen und mit dem yandex translator übersetzt. Für beides werden gültige Keys benötigt.
function get_rezept(frucht){
    var r_id;
    var rezept_text;
    var img_url;
    var min=1; 
    var max=5;  
    var zufall = Math.floor(Math.random() * (+max - +min)) + +min;
    var htlm_rezept_text;
            //API Food2Fork get id
            $.get(
                'https://www.food2fork.com/api/search',{
                q: frucht,
                count: 1,
                page: zufall,
                sort: 'r',
                key: 'Hier ein gültiger Schlüssel'
                },
                function(data){
                    var output; 
                    output = data.slice(data.search(/recipe_id":/) , data.search(/, "image_url"/));
                    r_id = output.slice(13,-1);

                    //API Food2Fork get recipe
                    $.get(
                    'https://www.food2fork.com/api/get',{
                    rId: r_id,
                    key: 'Hier ein gültiger Schlüssel'
                    },
                    function(data2){
                        rezept_text = data2.slice(data2.search(/"ingredients":/), data2.search(/, "source_url":/));
                        rezept_text = rezept_text.concat(" "+data2.slice(data2.search(/"title":/), ));
                        img_url = data2.slice(data2.search(/image_url":/), data2.search(/", "social_rank":/));
                        img_url = img_url.slice(13,);
                        
                        // yandex trans api
                        $.get(
                            'https://translate.yandex.net/api/v1.5/tr.json/translate',{
                            text: rezept_text,
                            lang: 'en-de',
                            format: 'html', 
                            key: 'Hier ein gültiger Schlüssel'
                            },
                            function(data3){
                                var string_data3 = JSON.stringify(data3);
                                string_data3 = '"'+string_data3+'"';
                                var titel; 
                                titel= string_data3.slice(string_data3.search(/Titel/),);
                                titel = titel.slice(11, -8);
                                var rezept_text; 
                                rezept_text = string_data3.slice(string_data3.search(/"Zutaten/), string_data3.search(/"Titel/));
                                rezept_text = "'"+rezept_text+"'";
                                rezept_text = rezept_text.replace('[', '');
                                rezept_text = rezept_text.replace(']', '');
                                rezept_text = rezept_text.replace(/\\/g, '');
                                rezept_text = rezept_text.split(/", /);
                                var i;
                                for (i = 0; i < rezept_text.length; i++) {
                                  htlm_rezept_text += rezept_text[i] + "<br>";
                                }
                                htlm_rezept_text = htlm_rezept_text.replace('undefined', '');
                                htlm_rezept_text = htlm_rezept_text.replace(/"/g, '');
                                htlm_rezept_text = htlm_rezept_text.replace("'Zutaten:","<b>Zutaten:</b> <br>");
                                htlm_rezept_text = htlm_rezept_text.replace(/'/, '');
                                htlm_rezept_text = htlm_rezept_text.replace(/ n /, '');
                                output = '<div><div class="fancyboxIframe" >' +
                                    '<a data-fancybox-type="iframe" class="fancyboxIframe" href="http://food2fork.com/view/' + r_id + '" target="_blank" ><img src="' + img_url + '" class="img-responsive thumbnail" ></a>' +
                                    '</div>' +
                                    '<div class=".fancyboxIframe2">' +
                                        '<h3 class="Vtitle fancyboxIframe2"><a data-fancybox-type="iframe" class="fancyboxIframe2" href="http://food2fork.com/view/' + r_id + '" target="_blank">' + titel + '</a></h3>'+
                                    '</div><div  id="cTitle"><i>'+htlm_rezept_text+'</i></div></div>' +
                                '<div class="clearfix"></div>';
                      //nachdem man alles erhalten hat wird es jetzt in die html geldaen
                      $('#rezept').append(output);
                                });
                        });
                    });
            }

//yandex Translator Api für die übersetzung des suchbegriffes
function trans (inhalt){
    $.get(
        'https://translate.yandex.net/api/v1.5/tr.json/translate',{
        text: inhalt,
        lang: 'de-en',
        format: 'html', 
        key: 'Hier ein gültiger Schlüssel'
        },
        function(data3){
            get_rezept(data3.text[0]);
        });

    
}

// die Wetter api von Openweathermap
function wetter_ddorf() {
	fetch('https://api.openweathermap.org/data/2.5/forecast?lat=51.2254&lon=6.7763&cnt=17&lang=de&appid=Hier ein gültiger Schlüssel')  
	.then(function(resp) { return resp.json() }) // Convert data to json
	.then(function(data) {
			$.each(data.list, function(index, val) {
				if (index == 0){
					var run = 1;
					wetter_ausgeben(val, run);
					}
				if (index == 8){
					var run = 2;
					wetter_ausgeben(val, run);
					}
				if (index == 16){
					var run = 3;
					wetter_ausgeben(val, run);
					}
				});
	});
}

function wetter_ausgeben( d, run){
    var celcius = Math.round(parseFloat(d.main.temp)-273.15);
	var iconcode = d.weather[0].icon;
	var iconurl = "http://openweathermap.org/img/w/" + iconcode + ".png";
	$('#wicon'+run).attr('src', iconurl);
	document.getElementById('description'+run).innerHTML = d.weather[0].description;
	document.getElementById('temp'+run).innerHTML = celcius + '&deg;';
	document.getElementById('location'+run).innerHTML = 'Düsseldorf';
	document.getElementById('datum'+run).innerHTML = d.dt_txt.slice(0,16)+' Uhr' ;
}