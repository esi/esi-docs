package sso

import cats.effect.Sync
import io.circe.generic.auto._
import io.circe.parser
import org.http4s.HttpRoutes
import org.http4s.dsl.Http4sDsl
import org.http4s.dsl.impl.QueryParamDecoderMatcher

import scala.util.control.NonFatal


object Routes {
  // This authorization code is a one time use only token that has a lifetime of 5 minutes.
  // If you do not respond within 5 minutes you will have to start over at step 1 again.
  private object CodeParamMatcher extends QueryParamDecoderMatcher[String]("code")

  private object StateParamMatcher extends QueryParamDecoderMatcher[String]("state")

  private case class AuthResponse(access_token: String, expires_in: Int, token_type: String, refresh_token: String)

  def ESICallback[F[_] : Sync](): HttpRoutes[F] = {
    val dsl = new Http4sDsl[F] {}
    import dsl._
    HttpRoutes.of[F] {
      case GET -> Root / "callback" :? CodeParamMatcher(code) +& StateParamMatcher(_) =>
        try {
          (for {
            response <- parser.decode[AuthResponse](ExampleSSO.authorize(code))
          } yield {
            myApplicationCodeHere(response.access_token, response.refresh_token)
            Ok(s"Success! Access Token: ${response.access_token}, Refresh Token: ${response.refresh_token}")
          }).getOrElse(BadRequest("Couldn't parse response from ESI SSO Authentication"))
        } catch {
          case NonFatal(e) =>
            BadRequest(e.getMessage)
        }
    }
  }

  private def myApplicationCodeHere(accessToken: String, refreshToken: String): Unit =
    println("now you can do whatever your app would normally do, and make requests to ESI using the tokens above!")
}
