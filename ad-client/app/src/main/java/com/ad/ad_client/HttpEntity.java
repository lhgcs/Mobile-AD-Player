package com.ad.ad_client;

import java.util.concurrent.TimeUnit;

import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

public class HttpEntity {
    private final int connectTiomeout = 10;
    private final int readTiomeout = 10;
    private String url;
    private OkHttpClient okHttpClient;
    private Request request;
    private Callback callback;

    public HttpEntity(String url, String json, Callback callback) {
        this.okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(connectTiomeout, TimeUnit.SECONDS)
                .readTimeout(readTiomeout, TimeUnit.SECONDS)
                .build();
        RequestBody body = RequestBody.create(MediaType.parse("application/json;"), json);
        this.request = new Request.Builder()
                .url(url)
                .method("post", body)
                .build();
        this.callback = callback;
    }
}
