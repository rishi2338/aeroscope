package com.aeroscope;

import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
@RequestMapping("/api")
public class MlController {
    private final WebClient client;
    public MlController(@Value("${ml.service-url:http://localhost:8000}") String url) {
        this.client = WebClient.builder().baseUrl(url).build();
    }
    @GetMapping("/health")
    public Map<?, ?> health() {
        return client.get().uri("/api/health").retrieve().bodyToMono(Map.class).block();
    }
    @PostMapping(value="/cluster", consumes=MediaType.MULTIPART_FORM_DATA_VALUE)
    public Map<?, ?> cluster(@RequestPart("file") MultipartFile file, @RequestParam(defaultValue="3") int clusters) throws Exception {
        MultipartBodyBuilder body = new MultipartBodyBuilder();
        body.part("file", new ByteArrayResource(file.getBytes()) { @Override public String getFilename() { return file.getOriginalFilename() == null ? "data.csv" : file.getOriginalFilename(); } });
        return client.post().uri(uri -> uri.path("/api/cluster").queryParam("clusters", clusters).build())
            .contentType(MediaType.MULTIPART_FORM_DATA).body(BodyInserters.fromMultipartData(body.build()))
            .retrieve().bodyToMono(Map.class).block();
    }
    @PostMapping(value="/forecast", consumes=MediaType.MULTIPART_FORM_DATA_VALUE)
    public Map<?, ?> forecast(@RequestPart("file") MultipartFile file, @RequestParam(defaultValue="PM2.5") String target, @RequestParam(defaultValue="7") int periods) throws Exception {
        MultipartBodyBuilder body = new MultipartBodyBuilder();
        body.part("file", new ByteArrayResource(file.getBytes()) { @Override public String getFilename() { return file.getOriginalFilename() == null ? "data.csv" : file.getOriginalFilename(); } });
        return client.post().uri(uri -> uri.path("/api/forecast").queryParam("target", target).queryParam("periods", periods).build())
            .contentType(MediaType.MULTIPART_FORM_DATA).body(BodyInserters.fromMultipartData(body.build()))
            .retrieve().bodyToMono(Map.class).block();
    }
}