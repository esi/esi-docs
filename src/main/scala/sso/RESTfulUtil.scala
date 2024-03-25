package sso

import requests.RequestBlob

object RESTfulUtil {
  def post(url: String,
           formData: Set[(String, String)],
           headers: Set[(String, String)] = Set.empty[(String, String)]
          ): String =
    requests.post(
      url = url,
      headers = headers,
      data = RequestBlob.FormEncodedRequestBlob(formData)
    ).text()
}
