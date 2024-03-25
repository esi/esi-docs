package sso

import cats.effect.{IO, IOApp}

import java.util.Base64
import scala.util.Random

object ExampleSSO extends IOApp.Simple {
  val run: IO[Nothing] = Server.run[IO] // starts the server that will listen for ESI to callback after you auth a character

  private val clientID = System.getProperty("client_id")
  private val redirectURI = "http%3A%2F%2Flocalhost%3A8080%2Fcallback" // http://locahost:8080/callback
  private val scopes = "publicData"
  private val (oneTimeUseVerifier, codeChallenge) = createOneTimeUseVerifierAndCodeChallenge()

  private val authorizationCodeUrl = s"https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri=$redirectURI&client_id=$clientID&scope=$scopes&code_challenge=$codeChallenge&code_challenge_method=S256&state=some_unique_string"
  println(s"Open this URL in your browser to authenticate with EVE Online SSO: $authorizationCodeUrl") // prints this out to the console so you can click it, which opens your web browser and allows you to auth your character

  private def createOneTimeUseVerifierAndCodeChallenge(bytes: Array[Byte] = Random.nextBytes(32)): (String, String) = {
    val encoded = base64UrlEncode(bytes)
    val oneTimeUseVerifier = encoded
    val sha256 = sha256Hash(oneTimeUseVerifier)
    val codeChallenge = base64UrlEncode(sha256).map(_.toChar).mkString
    (oneTimeUseVerifier.map(_.toChar).mkString, codeChallenge)
  }

  private def sha256Hash(bytes: Array[Byte]) =
    java.security.MessageDigest.getInstance("SHA-256").digest(bytes)

  /**
   * Since Base64.getUrlEncoder doesn't encode correctly, we use our own implementation here
   */
  private def base64UrlEncode(bytes: Array[Byte]): Array[Byte] =
    Base64.getEncoder.encode(bytes).map(_.toChar).collect {
      case char if char == '=' => None
      case char if char == '+' => Some('-')
      case char if char == '/' => Some('_')
      case char => Some(char)
    }.flatten.mkString.getBytes

  def authorize(code: String): String = {
    val url = s"https://login.eveonline.com/v2/oauth/token"
    val headers = Set(
      ("Content-Type", "application/x-www-form-urlencoded"),
      ("Host", "login.eveonline.com"),
    )
    val formData = Set(("grant_type", "authorization_code"), ("code", code), ("client_id", clientID), ("code_verifier", oneTimeUseVerifier))
    RESTfulUtil.post(url, formData, headers)
  }
}
