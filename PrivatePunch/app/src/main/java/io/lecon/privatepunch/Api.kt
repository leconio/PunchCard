package io.lecon.privatepunch

import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST


interface Api {

    @POST("setVerifyCode")
    @Headers(value = ["Content-Type: application/json", "Accept: application/json"])
    fun postVerifyCode(@Body code: RequestBody): Call<LoginActivity.RespBean>

}