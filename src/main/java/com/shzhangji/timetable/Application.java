package com.shzhangji.timetable;

import java.util.Arrays;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.oauth2.client.EnableOAuth2Sso;
import org.springframework.boot.autoconfigure.security.oauth2.resource.AuthoritiesExtractor;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.authority.AuthorityUtils;

@SpringBootApplication
@EnableOAuth2Sso
public class Application extends WebSecurityConfigurerAdapter {

	@Value("${timetable.admin}")
	private String admin;

	@Override
	protected void configure(HttpSecurity http) throws Exception {
		http.authorizeRequests().antMatchers("/**").hasRole("ADMIN");
	}

	@Bean
	public AuthoritiesExtractor authoritiesExtractor() {
		return map -> {
			Set<String> admins = Arrays.stream(admin.split(",")).collect(Collectors.toSet());
			String role = admins.contains(map.get("login")) ? "ADMIN" : "USER";
			return AuthorityUtils.createAuthorityList("ROLE_" + role);
		};
	}

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

}
