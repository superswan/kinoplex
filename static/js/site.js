        $(document).ready(function() {

            namespace = '/chat';
            var socket = io(namespace);
            var room = 'chat';

                        
            // Join the chat
            $('form#join').submit(function(event) {
                let username = $('#username').val();
                socket.emit('join', {'username': username, 'room': room});
                socket.emit('broadcast', {'data': username + ' has joined ' + room});
                $('#messages').css("display", "initial");
                $('form#send_msg').css("display", "initial");
                $('#joinbox').css("display", "none")

                return false;
            });
            
            // Initialize connection to chat server
            socket.on('connection', socket => {
              $('#messages').append('connected to chat...'+"<br>");
              socket.join(room)
            })
            
            // Hide messagebox until username is set
            // Establish new session
            socket.on('create_connection', function(data){
                username = data.username
                console.log(username)
                if (username == 'null') {
                $('#messages').css("display", "none");
                $('form#send_msg').css("display", "none");
                } else { 
                          $('#joinbox').css("display", "none");
                          socket.emit('join', {username: username, room: room})
                          socket.emit('load_chat_history')
                          socket.emit('broadcast', {'data': username + ' has joined ' + room});
                        }
              });

            // Post message to chat box
            socket.on('post_msg', function(msg) {
                $('#messages').append(msg.username + ": " + msg.message+"<br>").html();
            });

            //Send Broadcast message from server
            socket.on('send_broadcast', function(msg) {
                $('#messages').append("<b>"+ msg.data +"</b><br>")
            });

            //Send message to chat
            $('form#send_msg').submit(function(event) {
                let message = $('#msg_data').val();
                socket.emit('send_msg', {data: message});
                return false;
            });

            // Load chat history
            socket.on('display_msg'), function(msg_list) {
              return false;
            }

        });