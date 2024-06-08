Link to website: https://ci9ma.fly.dev/  
Account: admin@123  
Password: 123123

Cài đặt môi trường:  
- Cài đặt fly.io: `pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"`  
- Thiết lập các biến môi trường:  
    `flyctl secrets set SUPABASE_URL=https://xktxghadxpjdfyarekii.supabase.co`    
    `flyctl secrets set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhrdHhnaGFkeHBqZGZ5YXJla2lpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTUwMTIzNTYsImV4cCI6MjAzMDU4ODM1Nn0._9AvJKiHTIvyIYaRN-u9KWRwYu3_lUXaq0_bvqEnFQE`  
-  Deploy: `fly deploy`
1.	Làm thế nào để xử lí lỗi trong KoaJS?
•	Sử dụng middleware để xử lý lỗi: sử dụng một middleware để bắt và xử lý lỗi. Middleware này cần được đặt trước tất cả các middleware khác để nó có thể bắt mọi lỗi phát sinh trong các middleware hoặc route phía sau.
•	Ví dụ:  
 '// Middleware xử lý lỗi tổng quát  
app.use(async (ctx, next) => {  
    try {  
      await next();  
    } catch (err) {  
      console.error('Lỗi tổng quát xảy ra:', err); // In lỗi ra console  
      ctx.status = 500;  
      ctx.body = 'Something went wrong!';  
    }  
  });  
    
  // Middleware xử lý route cụ thể và lỗi cục bộ  
  app.use(async (ctx) => {  
    try {  
      // Giả sử có một lỗi phát sinh ở đây  
      throw new Error('Oops!');  
    } catch (err) {  
      console.error('Lỗi cục bộ xảy ra:', err); // In lỗi ra console  
      ctx.status = 400;  
      ctx.body = 'Custom error message';  
    }  
  });'  
•	Quy trình:
-	Khi có lỗi xảy ra trong middleware thứ hai, lỗi đó sẽ được bắt và in ra console với thông điệp "Lỗi cục bộ xảy ra:".
-	Nếu có lỗi không được bắt trong middleware thứ hai, middleware đầu tiên sẽ bắt lỗi đó, in ra console với thông điệp "Lỗi tổng quát xảy ra:", và trả về thông điệp lỗi tổng quát.
 
2.  Cách sử dụng Koa Router để quản lý định tuyến:
•	Cài đặt Koa Router
 
•	Tạo ứng dụng Koa và định nghĩa các route:
 
•	Để quản lý các route một cách có tổ chức, bạn có thể chia các route ra thành nhiều tệp riêng biệt. Ví dụ, tạo thư mục routes và tạo các tệp home.js và user.js trong đó.
•	Sử dụng Koa Router giúp bạn quản lý các route một cách có tổ chức và dễ bảo trì. Việc chia nhỏ các route theo chức năng và định nghĩa chúng trong các tệp riêng biệt giúp mã nguồn của bạn rõ ràng và dễ quản lý hơn. Koa Router cũng cung cấp nhiều tính năng mạnh mẽ như middleware, route nesting (lồng các route), và xử lý phương thức HTTP một cách hiệu quả. 
3. Các tính năng nổi bật của middleware trong KoaJS:
•	Sử dụng Async/Await Natively:
-	KoaJS sử dụng hoàn toàn async/await để xử lý bất đồng bộ, mang lại cú pháp đơn giản và dễ hiểu hơn so với cách tiếp cận dựa trên Callback hoặc Promise chaining.
-	Điều này giúp mã nguồn dễ đọc, dễ bảo trì và tránh các vấn đề về "Callback hell" hay "Promise chaining".
•	Xử lý lỗi tích hợp: KoaJS tích hợp sẵn khả năng xử lý lỗi trong luồng middleware thông qua cơ chế try/catch. Điều này giúp việc quản lý và xử lý lỗi trở nên nhất quán và đơn giản hơn.
•	Kiến trúc middleware xếp chồng (stacked middleware): Koa sử dụng kiến trúc middleware dạng "onion" (củ hành), nơi mỗi middleware có thể chạy cả trước và sau khi các middleware kế tiếp thực hiện. Điều này mang lại sự linh hoạt và kiểm soát tốt hơn về luồng xử lý yêu cầu và phản hồi.
•	Context Object: KoaJS sử dụng một context object (ctx) thống nhất để chứa thông tin về request và response, giúp truy cập và thao tác với các thông tin này trở nên trực quan và nhất quán hơn.
•	Không có built-in middleware: KoaJS không có built-in middleware như các framework khác, điều này cho phép người dùng tự tạo ra các middleware theo nhu cầu cụ thể của họ mà không bị ràng buộc bởi các middleware đi kèm.
