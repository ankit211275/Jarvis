$(document).ready(function () {
  $('.text').textillate({
    loop: true,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  // Siri configuration
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: '2',
    speed: '0.30',
    autostart: true
  });

  // Siri message animation
  $('.siri-message').textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true
    },
    out: {
      effect: "fadeOutUp",
      sync: true
    },
  });

  // Mic-button click event
  var mic_start_audio = new Audio("assets/sound/start_sound.mp3");

  $("#MicBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    // Play the audio
    mic_start_audio.play()
      .then(function () {
        // After the audio finishes playing, call the allcommand function
        eel.allCommands()();
      })
      .catch(function (error) {
        console.error("Error playing audio:", error);
        // Even if there's an error with the audio, still proceed to take the command
        eel.allCommands()();
      });
  });

  $(document).on('keydown', function(e) {
    console.log('Key down:', e.key, 'Meta key:', e.metaKey);

    if (e.key === 'j' && e.metaKey) {
      e.preventDefault(); // Prevent the default action if needed
      console.log('Command + J detected');
      // Your custom code here, e.g., toggle visibility, play audio, etc.
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);

      // Play the audio
      mic_start_audio.play()
        .then(function () {
          // After the audio finishes playing, call the allCommands function
          eel.allCommands()();
        })
        .catch(function (error) {
          console.error("Error playing audio:", error);
          // Even if there's an error with the audio, still proceed to take the command
          eel.allCommands()();
        });
    }
  });

    function PlayAssistant(message){
      if(message!= ""){
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands(message);
        $("$chatbox").val("")
        $("#MicBtn").attr("hidden", false);
        $("#SendBtn").attr("hidden", true);
      }
    }

    function showHideButton(message){
      if(message.length==0){
        $("#MicBtn").attr('hidden', false);
        $("#SendBtn").attr('hidden', true);
      }
      else{
        $("#MicBtn").attr('hidden', true);
        $("#SendBtn").attr('hidden', false);
      }
    }

    $("#chatbox").keyup(function(){
      let message=$("#chatbox").val();
      showHideButton(message)
    });

    $("#SendBtn").click(function(){
      let message=$("#chatbox").val();
      PlayAssistant(message)
    });

    $("#chatbox").keypress(function(e){
      key=e.which;
      if(key==13){
        let message=$("#chatbox").val();
        PlayAssistant(message)
      }
    });
    
});
