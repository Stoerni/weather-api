<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

// 🔑 Hier nicht direkt den Key einfügen!
$apiKey = getenv("OPENWEATHER_KEY");

$city = $_GET["city"] ?? "Barcelona";
$city = preg_replace("/[^a-zA-ZäöüÄÖÜß\s-]/", "", $city);

if (strlen($city) > 50) {
    http_response_code(400);
    echo json_encode(["error" => "Ungültige Stadt"]);
    exit;
}

$url = "https://api.openweathermap.org/data/2.5/weather?q=" .
        urlencode($city) .
        "&appid=$apiKey&units=metric&lang=de";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($ch);

if(curl_errno($ch)) {
    http_response_code(500);
    echo json_encode(["error" => curl_error($ch)]);
    exit;
}

curl_close($ch);
echo $response;