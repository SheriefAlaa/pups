/**
 * "Hey there, I'm PRODROMUS, a very simple XMPP messaging client, 
 * mainly reasonable as contact form replacement/supplement or 
 * support contact utility."
 * 
 * (c) 2009-10 by Raphael Kallensee, http://raphael.kallensee.name
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 * 
 * PRODROMUS uses jQuery, which is available under the MIT or GPL Version 2 
 * licenses. Secondly this little piece of software uses the great Strophe.js
 * library which is available under the MIT license, except for two functions
 * which are licensed as public domain and BSD. Additionally a Date.format
 * function is used which is available under the MIT license.
 *
 * jQuery: http://jquery.com 
 * Strophe.js: http://code.stanziq.com/strophe/
 */

/**
 * Prodromus class
 *
 * Serves as a namespace for all methods and functions
 * 
 * @license Affero General Public License
 */

/*
* 2 = Something is really wrong with the server
* 1 = available/chat
* 0 = unavailable/away/dnd/xa
*/

var isAvailable = null;
var status_msg = null;

$(document).ready( function() {
    Prodromus.UI.initialize( $( Prodromus.config.TARGET_ELEMENT ) );
    
    Prodromus.connection = new Strophe.Connection( Prodromus.config.BOSH_SERVICE );
    

    // Start checking if the support assistant is present and ready for chatting.
    Prodromus.PresenceReporter.freeze_controls(true);    
    Prodromus.connection.connect( Prodromus.config.XMPP_SERVER, '', get_status);


    // Uncomment the following lines to spy on the wire traffic.
    //Prodromus.connection.rawInput = function (data) { Prodromus.UI.log('RECV: ' + data, 'system'); };
    //Prodromus.connection.rawOutput = function (data) { Prodromus.UI.log('SEND: ' + data, 'system'); };

    // Uncomment the following line to see all the debug output.
    //Strophe.log = function (level, msg) { Prodromus.UI.log('LOG: ' + msg, 'system'); };
    
    $('#prodromus-messaging').hide();

    $('#prodromus-connect').bind( 'click', function( e ) {
	    Prodromus.actionhandler.connect();
    });
    
    $('#prodromus-msgform').bind( 'submit', function( e ) {
        return Prodromus.actionhandler.sendmessage();
    });
    
    $('#prodromus-login').bind( 'submit', function( e ) {
        return Prodromus.actionhandler.connect();
    });
    
    
    $('#prodromus-message').bind( 'keyup', function( e ) {
        return Prodromus.actionhandler.messagekeyup( e );
    });
    
    $('#prodromus-sendmessage').bind( 'click', function( e ) {
        Prodromus.actionhandler.sendmessage();
    });
});

$(window).unload( function() {
    Prodromus.connection.disconnect();
});

Prodromus.Util = {
    
    text2link: function( text )
    {
        if( !text ) {
            return text;
        }
        
        text = text.replace(
            /((https?\:\/\/|ftp\:\/\/)|(www\.))(\S+)(\w{2,4})(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/gi
          , function( url ) {
                nice = url;
                if( url.match( "^https?:\/\/" ) ) {
                    nice = nice.replace( /^https?:\/\//i, "" )
                } else {
                    url = 'http://'+url;
                }			
                return '<a target="_blank" href="' + url + '">' + nice.replace( /^www./i, "" ) + '</a>';
		    }
		);
		
		return text;
	},
	
	htmlspecialchars: function( text ) {
        text = text.replace(/\&/g, "&amp;");
        text = text.replace(/</g,  "&lt;");
        text = text.replace(/>/g,  "&gt;");
        text = text.replace(/'/g,  "&#39;");
        
        return text;
    }
	
}

Prodromus.buildAndSendMessage = function( message, type ) {

    var msg = $msg({from: Prodromus.connection.jid, to: Prodromus.config.RECEIVER, type: type})
        .c("body").t(message).up()
        .c("active", {xmlns: "http://jabber.org/protocol/chatstates"});
    
    // TODO: add real support for XEP-0085 (Chat State Notifications)

    Prodromus.connection.send( msg );

    Prodromus.UI.log( message, "msgOut" );
}

Prodromus.actionhandler = {
    connect: function() {
        if( $('#prodromus-username').val() != '' ) {
            var button = $('#prodromus-connect');
	        if( button.val() == Prodromus.i18n.t9n( 'connect' ) ) {
	            button.val( Prodromus.i18n.t9n( 'disconnect' ) );
	            $('#prodromus-usernameDisplay').text( $('#prodromus-username').val() );
	            $('#prodromus-username').hide();
	            
	            Prodromus.config.SENDERNAME = $('#prodromus-username').val();
	            Prodromus.connection.connect( Prodromus.config.XMPP_SERVER, '', Prodromus.actionhandler.onConnect );
	        } else {
	            button.val( Prodromus.i18n.t9n( 'connect' ) );
	            
	            Prodromus.buildAndSendMessage( 
	                Prodromus.Util.htmlspecialchars( Prodromus.config.SENDERNAME ) + Prodromus.i18n.t9n( 'msg-goodbye' )
	              , 'chat' 
                );
	            setTimeout( 'Prodromus.connection.disconnect();', 1000 );
	        }
	    }
        return false;
    },
    
    messagekeyup: function( e ) {
        if( e.which == 13 ) {
            Prodromus.actionhandler.sendmessage();
	    }
	    
	    // TODO: add real support for XEP-0085 (Chat State Notifications)
	    
	    return true;
    },

    sendmessage: function() {
        $('#prodromus-message').val( 
            $('#prodromus-message').val().replace(/\n/g,"").replace(/\r/g,"")
        );
        
        if( $('#prodromus-message').val() != '' ) {
            Prodromus.buildAndSendMessage( $('#prodromus-message').val(), 'chat' );
	        $('#prodromus-message').val('');
	    }
        return false;
    },
    
    onConnect: function( status ) {
        switch( status ) {
            case Strophe.Status.CONNECTING:
                $('#prodromus-messaging').slideDown();
                Prodromus.UI.log( Prodromus.i18n.t9n( 'connecting' ), 'system' );
                break;
            case Strophe.Status.CONNFAIL:
                Prodromus.UI.log( Prodromus.i18n.t9n( 'failed-to-connect' ), 'system' );
                $('#prodromus-connect').val() = Prodromus.i18n.t9n( 'connect' );
                $('#prodromus-username').get(0).readOnly = false;
                $('#prodromus-messaging').slideUp();
                break;
            case Strophe.Status.DISCONNECTING:
                Prodromus.UI.log( Prodromus.i18n.t9n( 'disconnecting' ), 'system' );
                break;
            case Strophe.Status.DISCONNECTED:
                Prodromus.UI.log( Prodromus.i18n.t9n( 'disconnected' ), 'system' );
                $('#prodromus-connect').val( Prodromus.i18n.t9n( 'connect' ) );
                $('#prodromus-username').get(0).readOnly = false;
                $('#prodromus-messaging').slideUp();
                break;
            case Strophe.Status.CONNECTED:
                Prodromus.UI.log( Prodromus.i18n.t9n( 'connected' ), 'system' );
                
                var username = $('#prodromus-username').get(0);
                username.readOnly = true;
                $('#prodromus-message').focus();

                Prodromus.connection.addHandler( 
                    Prodromus.actionhandler.onMessage, null, 'message'
                ); 
                Prodromus.connection.send( $pres() );

                Prodromus.buildAndSendMessage(
                    Prodromus.Util.htmlspecialchars( Prodromus.config.SENDERNAME ) + Prodromus.i18n.t9n( 'msg-hello' ) + " Token: " + Prodromus.config.TOKEN
                  , 'chat' 
                );
                break;
        }
    },

    onMessage: function( msg ) {
        if( $(msg).attr('type') == "chat" && $(msg).find('body').size() > 0 ) {
	        Prodromus.UI.log( $(msg).find('body').first().text(), 'msgIn' );
        }

        // we must return true to keep the handler alive.  
        // returning false would remove it after it finishes.
        return true;
    }
}


Prodromus.UI = {

    initialize: function( el ) {
        var pattern = 
             '<div id="prodromus-login">'
                +'<form name="prodromus-credentials" action="">'
                    +'<input type="button" id="prodromus-connect" value="{t9n_connect}" />'
                    +'<label for="prodromus-username">{t9n_your-name}:</label>'
                    +'<input type="text" id="prodromus-username" value="{sendername}" />'
                    +'<span id="prodromus-usernameDisplay"></span>'
                    +'<div class="clear"></div>'
                +'</form>'
            +'</div>'
            +'<div id="prodromus-messaging">'
                +'<div id="prodromus-log"></div>'
                +'<form id="prodromus-msgform" action="">'
                    +'<textarea id="prodromus-message" rows="2" cols="52"></textarea>'
                    +'<input type="button" id="prodromus-sendmessage" value="{t9n_send}" />'
                    +'<div class="prodromus-clear"></div>'
                +'</form>'
            +'</div>';
        
        pattern = pattern.replace( "{sendername}", Prodromus.config.SENDERNAME );
        pattern = pattern.replace( "{t9n_your-name}", Prodromus.i18n.t9n( 'your-name' ) );
        pattern = pattern.replace( "{t9n_connect}", Prodromus.i18n.t9n( 'connect' ) );
        pattern = pattern.replace( "{t9n_send}", Prodromus.i18n.t9n( 'send' ) );
            
        $(el).html( pattern );
    },
    
    log: function( msg, type ) {
        var pattern = 
             '<div class="message message{type}">' 
                +'<span class="msgText">{message}</span>'
                +'<span class="msgPerson"><b>{person}</b><span class="msgTime">, {time}</span></span>'
            +'</div>';
        
        switch( type ) {
            case 'msgIn':
                pattern = pattern.replace( "{type}", "In" );
                pattern = pattern.replace( "{person}", Prodromus.Util.htmlspecialchars( Prodromus.config.RECEIVERNAME ) );
                break;
            case 'msgOut':
                pattern = pattern.replace( "{type}", "Out" );
                pattern = pattern.replace( "{person}", Prodromus.Util.htmlspecialchars( Prodromus.config.SENDERNAME ) );
                break;
            case 'system':
            default:
                pattern = pattern.replace( "{type}", "System" );
                pattern = pattern.replace( "{person}", "System" );
                break;
        }
        
        msg = Prodromus.Util.htmlspecialchars( msg );
        msg = Prodromus.Util.text2link( msg );
        
        pattern = pattern.replace( "{message}", msg );
        
        pattern = pattern.replace( "{time}", Prodromus.i18n.getFormattedDate() );
        $( pattern ).appendTo( $('#prodromus-log') );
        
        $("#prodromus-log").animate( { scrollTop: $("#prodromus-log").prop("scrollHeight") }, 1000 );
    }

}

Prodromus.i18n = {

    getFormattedDate: function() {
        return new Date().format( Prodromus.config.DATEFORMAT );
    },
    
    t9n: function( key ) {
        return Prodromus.t9n[ Prodromus.config.LANGUAGE ][ key ];
    }

}

Prodromus.t9n = {

    'de': {
        'your-name': 'Ihr Name',
        'connect': 'Verbinden',
        'connecting': 'Verbindung wird hergestellt...',
        'connected': 'Verbunden!',
        'disconnect': 'Verbindung trennen',
        'disconnecting': 'Verbindung wird getrennt...',
        'disconnected': 'Verbindung getrennt.',
        'send': 'Senden',
        'failed-to-connect': 'Es konnte keine Verbindung zum Server aufgebaut werden!',
        'msg-hello': ' startete eine Unterhaltung.',
        'msg-goodbye': ' verlässt die Unterhaltung.'
    },
    
    'en': {
        'your-name': 'Your name',
        'connect': 'connect',
        'connecting': 'Connecting...',
        'connected': 'Connected!',
        'disconnect': 'disconnect',
        'disconnecting': 'Disconnecting...',
        'disconnected': 'Disconnected.',
        'send': 'Send',
        'failed-to-connect': 'Failed to connect to the server!',
        'msg-hello': ' joins the chat.',
        'msg-goodbye': ' leaves the chat. '
    }

}

// Simulates PHP's date function
// @see http://jacwright.com/projects/javascript/date_format
// Licensed under a MIT license.
Date.prototype.format = function(format) {
	var returnStr = '';
	var replace = Date.replaceChars;
	for (var i = 0; i < format.length; i++) {
		var curChar = format.charAt(i);
		if (replace[curChar]) {
			returnStr += replace[curChar].call(this);
		} else {
			returnStr += curChar;
		}
	}
	return returnStr;
};

Date.replaceChars = {
	shortMonths: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
	longMonths: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
	shortDays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
	longDays: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
	
	// Day
	d: function() { return (this.getDate() < 10 ? '0' : '') + this.getDate(); },
	D: function() { return Date.replaceChars.shortDays[this.getDay()]; },
	j: function() { return this.getDate(); },
	l: function() { return Date.replaceChars.longDays[this.getDay()]; },
	N: function() { return this.getDay() + 1; },
	S: function() { return (this.getDate() % 10 == 1 && this.getDate() != 11 ? 'st' : (this.getDate() % 10 == 2 && this.getDate() != 12 ? 'nd' : (this.getDate() % 10 == 3 && this.getDate() != 13 ? 'rd' : 'th'))); },
	w: function() { return this.getDay(); },
	z: function() { return "Not Yet Supported"; },
	// Week
	W: function() { return "Not Yet Supported"; },
	// Month
	F: function() { return Date.replaceChars.longMonths[this.getMonth()]; },
	m: function() { return (this.getMonth() < 9 ? '0' : '') + (this.getMonth() + 1); },
	M: function() { return Date.replaceChars.shortMonths[this.getMonth()]; },
	n: function() { return this.getMonth() + 1; },
	t: function() { return "Not Yet Supported"; },
	// Year
	L: function() { return "Not Yet Supported"; },
	o: function() { return "Not Supported"; },
	Y: function() { return this.getFullYear(); },
	y: function() { return ('' + this.getFullYear()).substr(2); },
	// Time
	a: function() { return this.getHours() < 12 ? 'am' : 'pm'; },
	A: function() { return this.getHours() < 12 ? 'AM' : 'PM'; },
	B: function() { return "Not Yet Supported"; },
	g: function() { return this.getHours() % 12 || 12; },
	G: function() { return this.getHours(); },
	h: function() { return ((this.getHours() % 12 || 12) < 10 ? '0' : '') + (this.getHours() % 12 || 12); },
	H: function() { return (this.getHours() < 10 ? '0' : '') + this.getHours(); },
	i: function() { return (this.getMinutes() < 10 ? '0' : '') + this.getMinutes(); },
	s: function() { return (this.getSeconds() < 10 ? '0' : '') + this.getSeconds(); },
	// Timezone
	e: function() { return "Not Yet Supported"; },
	I: function() { return "Not Supported"; },
	O: function() { return (-this.getTimezoneOffset() < 0 ? '-' : '+') + (Math.abs(this.getTimezoneOffset() / 60) < 10 ? '0' : '') + (Math.abs(this.getTimezoneOffset() / 60)) + '00'; },
	T: function() { var m = this.getMonth(); this.setMonth(0); var result = this.toTimeString().replace(/^.+ \(?([^\)]+)\)?$/, '$1'); this.setMonth(m); return result;},
	Z: function() { return -this.getTimezoneOffset() * 60; },
	// Full Date/Time
	c: function() { return "Not Yet Supported"; },
	r: function() { return this.toString(); },
	U: function() { return this.getTime() / 1000; }
};


Prodromus.PresenceReporter =

{
    subscribe: function()
    {
        data = 
        {
            jid: Prodromus.config.RECEIVER,
            name: Prodromus.config.RECEIVERNAME
        }

    var subscribe = $pres({to: data.jid, "type": "subscribe"});
    Prodromus.connection.send(subscribe);

    },

    get_pres: function()
    {
        iq = $iq({type: 'get'}).c('query', {xmlns: 'jabber:iq:roster'});
        Prodromus.connection.sendIQ(iq, Prodromus.PresenceReporter.get_roster);
    },

    get_roster: function(iq)
    {
        Prodromus.connection.addHandler(Prodromus.PresenceReporter.on_presence, null, "presence");
        Prodromus.connection.send($pres());
    },

    on_presence: function(presence)
    {
        var presence_type = $(presence).attr('type'); // unavailable, subscribed, etc...
        var from = $(presence).attr('from'); // the jabber_id of the contact
        var to = $(presence).attr('to');
        var show = $(presence).find("show").text(); // this is what gives away, dnd, etc.
        msg = $(presence).find("status").text();
        // console.log(presence);
        // console.log("presence_type : " + presence_type );
        // console.log("Show: " + show );
        // console.log("status : " + msg );
        // console.log("From: " + from );
        // console.log("To: " + to);

        if ( to !== undefined )
        {
            if (presence_type != 'error')
            {
                // Save status messge if it exists
                if (msg !== null && msg !== '' && msg !== undefined)
                    status_msg = msg;

                // Available
                if ( (presence_type === undefined) && (show === '' || show === 'chat') )
                {
                    isAvailable = 1;
                    return true;
                }

                // Not Available
                if (presence_type === 'unavailable' || show === 'xa' || show === 'dnd' || 'away')
                {
                    isAvailable = 0;
                    return true;
                }
            }
            else
            {
                isAvailable = 2; // Server problem
            }
        }
        return true;
    },

    freeze_controls: function(bool)
    {
        $('#prodromus-username').prop( "disabled", bool );
        $('#prodromus-connect').prop( "disabled", bool );
    }
};

// Get current support assistant status
function get_status(status) {
    if (status === Strophe.Status.CONNECTED)
    {
        Prodromus.PresenceReporter.subscribe();
        Prodromus.PresenceReporter.get_pres();
        wait();
    }

    if (status === Strophe.Status.DISCONNECTED)
    {
        if (isAvailable == 1)
            Prodromus.PresenceReporter.freeze_controls(false);

        give_feedback();
    }
}

// Do not dissconnect until isAvailable is populated.
function wait()
{
    if (isAvailable == null)
        setTimeout(wait, 500);
    else
        Prodromus.connection.disconnect();
}

function give_feedback()
{
    if (isAvailable !== 1)
    {
        if (status_msg !== null)
            alert(Prodromus.config.RECEIVERNAME + "'s status: " + status_msg);
        else
            alert(Prodromus.config.RECEIVERNAME + " is not available at the moment.");
    }
}