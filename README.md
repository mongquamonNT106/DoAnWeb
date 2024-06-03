Link to website: https://ci9ma.fly.dev/  
Account: admin@123  
Password: 123123

Cài đặt môi trường:  
- Cài đặt fly.io: pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"  
- Thiết lập các biến môi trường:
    `flyctl secrets set SUPABASE_URL=https://xktxghadxpjdfyarekii.supabase.co`    
    `flyctl secrets set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhrdHhnaGFkeHBqZGZ5YXJla2lpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTUwMTIzNTYsImV4cCI6MjAzMDU4ODM1Nn0._9AvJKiHTIvyIYaRN-u9KWRwYu3_lUXaq0_bvqEnFQE`  
-  Deploy: `fly deploy`
