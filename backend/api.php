<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

function getSoundcloudData($url) {

    $curl = curl_init();

    curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => $url
    ));

    $response = curl_exec($curl);

    curl_close($curl);

    return $response;

}

function getTrack($emotion) {

    $response = getSoundcloudData("http://api.soundcloud.com/tracks?client_id=000b1c01843b18b6ef32eec96ce1fe86&tags=$emotion");

    $json  = json_decode($response,$assoc = TRUE);

    //Making track JSON
    $tracks_array = array("queue" => array(), "mood" => $emotion);

    for ($x = 0; $x < count($json); $x++) {

        $title = $json[$x]["title"];

        if (isset($json[$x]["username"])) {
            $artist = $json[$x]["username"];
        } else {
            $artist = "";
        }

        $artwork_url = $json[$x]["artwork_url"];
        $duration = $json[$x]["duration"];
        $stream_url = $json[$x]["stream_url"] . "?client_id=000b1c01843b18b6ef32eec96ce1fe86";

        //Array to append
        $song = array("title" => $title, "artist" => $artist, "artwork_url" => $artwork_url, "duration" => $duration, "stream_url" => $stream_url);

        array_push($tracks_array["queue"], $song);

    }

    $tracks_json = json_encode($tracks_array);

    #Storing the songs to JSON text file.
    $serialise = serialize($tracks_array);

    #Writing to file.
    $file = fopen("songs.txt", "w");

    fwrite($file, $serialise);

    fclose($file);

    //Returning URLs
    return $tracks_json;

}

getTrack("happy");

//Updates the UI with current songs.
function updateUI() {

    $file = fopen("songs.txt", "r");

    $output = unserialize(fread($file,filesize("songs.txt")));

    return json_encode($output);

}

function controls() {
    return;
}

#Case Statement that handles JSON too.
switch ($_GET['action']) {

    //Registration Functions.
    case 'getTrack':
        #Retrieving the data
        $emotion = $_GET["emotion"];
        echo(getTrack($emotion));
        break;

    case 'updateUI':
        echo(updateUI());
        break;

    case 'control':
        $command = $_GET["command"];
        return updateUI();
        break;
}

?>
