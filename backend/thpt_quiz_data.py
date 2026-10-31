# -*- coding: utf-8 -*-
"""
thpt_quiz_data.py - Ngân hàng 100 câu hỏi trắc nghiệm Ôn thi Tốt nghiệp THPT Quốc Gia môn Tin học (Chuẩn GDPT 2018).
Gồm 5 chuyên đề cốt lõi, mỗi chuyên đề 20 câu hỏi chọn lọc có bẫy thi và phân tích lỗi sai kinh điển của học sinh.
"""

THPT_QUIZZES = {
    # =========================================================================
    # CHUYÊN ĐỀ 1: MẠNG MÁY TÍNH VÀ INTERNET (20 CÂU)
    # =========================================================================
    "1": {
        "topic_id": "1",
        "topic_title": "Chuyên đề 1: Mạng máy tính và Internet",
        "description": "20 câu hỏi trọng tâm bám sát ma trận đề thi tốt nghiệp THPT: Thiết bị mạng, giao thức IP/TCP/UDP, mô hình phân cấp, dịch vụ mạng và các bẫy khái niệm hay gặp.",
        "questions": [
            {
                "id": 1,
                "question": "Thiết bị mạng nào sau đây có chức năng định tuyến các gói tin giữa các mạng khác nhau dựa trên địa chỉ IP?",
                "options": [
                    "A. Hub (Bộ chia)",
                    "B. Switch (Bộ chuyển mạch)",
                    "C. Router (Bộ định tuyến)",
                    "D. Repeater (Bộ lặp)"
                ],
                "answer": 2,
                "trap": "Học sinh hay nhầm Switch và Router. Switch chỉ chuyển tiếp dữ liệu trong NỘI BỘ một mạng cục bộ (LAN) dựa vào địa chỉ MAC. Chỉ có Router mới kết nối các mạng KHÁC NHAU (như nối mạng gia đình ra Internet) bằng địa chỉ IP.",
                "explanation": "Router (Bộ định tuyến) hoạt động ở tầng Mạng (Network Layer), có bảng định tuyến để tìm đường đi tối ưu cho gói tin giữa các mạng khác nhau."
            },
            {
                "id": 2,
                "question": "Phát biểu nào sau đây là ĐÚNG khi nói về mối quan hệ giữa Internet và World Wide Web (WWW)?",
                "options": [
                    "A. Internet và World Wide Web là hai tên gọi khác nhau của cùng một hệ thống mạng.",
                    "B. World Wide Web là mạng hạ tầng vật lý, còn Internet là dịch vụ truyền thông tin trên đó.",
                    "C. Internet là mạng toàn cầu kết nối các máy tính, còn World Wide Web là một dịch vụ thông tin chạy trên Internet.",
                    "D. World Wide Web ra đời trước và là nền tảng để các kỹ sư xây dựng nên mạng Internet."
                ],
                "answer": 2,
                "trap": "Học sinh rất hay đồng nhất Internet và Web. Web chỉ là một trong nhiều dịch vụ (cùng với Email, FTP, VoIP, IoT) chạy trên nền tảng hạ tầng Internet.",
                "explanation": "Internet là mạng lưới các mạng máy tính kết nối toàn cầu (hạ tầng). World Wide Web (WWW) là dịch vụ siêu văn bản kết nối các trang web thông qua giao thức HTTP/HTTPS chạy trên nền hạ tầng đó."
            },
            {
                "id": 3,
                "question": "Trong các địa chỉ IPv4 dưới đây, địa chỉ nào KHÔNG HỢP LỆ?",
                "options": [
                    "A. 192.168.1.1",
                    "B. 10.0.0.254",
                    "C. 172.16.256.5",
                    "D. 8.8.8.8"
                ],
                "answer": 2,
                "trap": "Học sinh nhìn lướt qua thấy 4 nhóm số quen thuộc mà không kiểm tra giá trị của từng byte. Mỗi octet trong IPv4 chỉ có 8 bit, giá trị chỉ được từ 0 đến 255. Số 256 vượt quá giới hạn.",
                "explanation": "Địa chỉ IPv4 gồm 4 byte, mỗi byte biểu diễn bằng số nguyên từ 0 đến 255 cách nhau bởi dấu chấm. Ở phương án C, số '256' là không hợp lệ."
            },
            {
                "id": 4,
                "question": "Một bạn học sinh kiểm tra địa chỉ IP của máy tính ở nhà thấy là 192.168.1.15. Khi đến trường, máy tính của bạn khác cũng có địa chỉ 192.168.1.15. Điều này giải thích như thế nào?",
                "options": [
                    "A. Hai máy tính đang bị xung đột IP và sẽ không thể kết nối mạng được.",
                    "B. Đây là địa chỉ IP riêng (Private IP), dùng trong mạng nội bộ nên có thể trùng nhau ở các mạng LAN độc lập.",
                    "C. Nhà mạng đã cấp nhầm một địa chỉ IP công cộng (Public IP) cho cả hai gia đình.",
                    "D. Một trong hai máy tính đã bị kẻ xấu giả mạo địa chỉ IP."
                ],
                "answer": 1,
                "trap": "Nhiều bạn nghĩ rằng mọi địa chỉ IP trên thế giới đều phải độc nhất không được trùng lặp. Điều đó chỉ đúng với IP công cộng (Public IP), còn IP riêng (Private IP) dùng trong mạng LAN thì mạng nào cũng dùng dải 192.168.x.x được.",
                "explanation": "Dải 192.168.0.0 - 192.168.255.255 là dải IP riêng (Private IP). Thiết bị định tuyến (Router) tại mỗi nhà sử dụng kỹ thuật NAT để chia sẻ 1 IP công cộng ra nhiều IP riêng nội bộ."
            },
            {
                "id": 5,
                "question": "Dịch vụ mạng DNS (Domain Name System) đóng vai trò gì trong hoạt động của Internet?",
                "options": [
                    "A. Chuyển đổi dữ liệu trang web từ ngôn ngữ HTML sang mã nhị phân.",
                    "B. Chuyển đổi tên miền dễ nhớ (ví dụ: google.com) thành địa chỉ IP tương ứng của máy chủ.",
                    "C. Cấp phát địa chỉ IP tự động cho các thiết bị khi tham gia vào mạng.",
                    "D. Mã hóa toàn bộ dữ liệu truyền giữa người dùng và máy chủ để bảo mật."
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm DNS với DHCP (cấp IP tự động) hoặc SSL/TLS (mã hóa). DNS giống như cuốn 'danh bạ điện thoại' của Internet, đổi tên người thành số máy.",
                "explanation": "DNS (Domain Name System) là hệ thống phân giải tên miền, giúp chuyển đổi tên miền dạng chữ dễ nhớ (như dantri.com.vn) thành địa chỉ IP số học để trình duyệt gửi gói tin tới đúng máy chủ."
            },
            {
                "id": 6,
                "question": "Khi xem video trực tiếp (livestream) hoặc gọi video call, giao thức tầng truyền vận nào thường được ưu tiên sử dụng và vì sao?",
                "options": [
                    "A. TCP, vì đảm bảo 100% dữ liệu không bị thất lạc và kiểm tra lỗi chặt chẽ.",
                    "B. UDP, vì tốc độ truyền nhanh, độ trễ thấp và chấp nhận mất mát một lượng nhỏ gói tin hình ảnh.",
                    "C. HTTP, vì đây là giao thức duy nhất hiển thị được video trên trình duyệt.",
                    "D. FTP, vì giao thức này chuyên truyền tải các file đa phương tiện dung lượng lớn."
                ],
                "answer": 1,
                "trap": "Học sinh thường nghĩ 'giao thức tốt nhất phải là giao thức không bao giờ làm mất dữ liệu' (TCP). Nhưng trong truyền phát trực tiếp thời gian thực, việc gửi lại gói tin bị mất sẽ gây giật lag nghiêm trọng, nên UDP mới là lựa chọn tối ưu.",
                "explanation": "UDP (User Datagram Protocol) không cần thiết lập kết nối trước, không gửi lại gói tin mất nên tốc độ truyền tải cực nhanh và độ trễ thấp, rất phù hợp cho livestream, voice chat và game online."
            },
            {
                "id": 7,
                "question": "Môi trường truyền dẫn nào sau đây truyền dữ liệu bằng tín hiệu ánh sáng, có tốc độ cao nhất và hoàn toàn không bị ảnh hưởng bởi nhiễu điện từ?",
                "options": [
                    "A. Cáp xoắn đôi UTP",
                    "B. Cáp đồng trục (Coaxial Cable)",
                    "C. Cáp sợi quang (Fiber Optic Cable)",
                    "D. Sóng vô tuyến Wi-Fi"
                ],
                "answer": 2,
                "trap": "Đề thi hay hỏi về ưu điểm 'không bị ảnh hưởng bởi sấm sét hoặc đường dây điện cao thế chạy song song'. Chỉ có cáp quang dùng ánh sáng phản xạ toàn phần trong lõi thủy tinh/nhựa nên miễn nhiễm với nhiễu điện từ.",
                "explanation": "Cáp quang sử dụng sợi thủy tinh hoặc nhựa tinh khiết để truyền tín hiệu dưới dạng xung ánh sáng, có băng thông cực lớn, suy hao thấp và không bị can nhiễu điện từ như cáp kim loại."
            },
            {
                "id": 8,
                "question": "Giao thức nào sau đây chịu trách nhiệm tự động cấp phát cấu hình mạng (địa chỉ IP, Subnet Mask, Gateway) cho thiết bị khi kết nối vào mạng?",
                "options": [
                    "A. DNS",
                    "B. DHCP",
                    "C. ARP",
                    "D. ICMP"
                ],
                "answer": 1,
                "trap": "Tránh nhầm lẫn chữ cái đầu D: DNS là phân giải tên miền (Domain Name), còn DHCP (Dynamic Host Configuration Protocol) là cấu hình máy chủ động (cấp IP).",
                "explanation": "DHCP (Dynamic Host Configuration Protocol) tự động gán địa chỉ IP tạm thời cho máy trạm giúp tiết kiệm IP và tránh việc người dùng phải cấu hình IP thủ công bằng tay."
            },
            {
                "id": 9,
                "question": "Một trang web có địa chỉ bắt đầu bằng 'https://' khác với 'http://' ở điểm quan trọng nào?",
                "options": [
                    "A. Trang web https luôn tải nhanh gấp đôi trang web http thông thường.",
                    "B. Trang web https sử dụng thêm tầng bảo mật SSL/TLS để mã hóa dữ liệu truyền giữa client và server.",
                    "C. Trang web https chỉ có thể xem được trên điện thoại thông minh, không xem được trên máy tính.",
                    "D. Trang web https là trang web thuộc các cơ quan chính phủ quản lý."
                ],
                "answer": 1,
                "trap": "Chữ 's' ở cuối https là viết tắt của 'Secure'. Nhiều học sinh nhầm 's' là Speed (tốc độ) hoặc Server.",
                "explanation": "HTTPS (HyperText Transfer Protocol Secure) sử dụng chứng chỉ số và giao thức mã hóa SSL/TLS để bảo vệ dữ liệu nhạy cảm (mật khẩu, tài khoản thẻ) khỏi bị đánh cắp trên đường truyền."
            },
            {
                "id": 10,
                "question": "Địa chỉ IPv6 có độ dài bao nhiêu bit và được viết bằng hệ cơ số nào?",
                "options": [
                    "A. 32 bit, viết bằng hệ thập phân chia làm 4 nhóm.",
                    "B. 64 bit, viết bằng hệ nhị phân chia làm 8 nhóm.",
                    "C. 128 bit, viết bằng hệ thập lục phân (Hexadecimal) chia làm 8 nhóm cách nhau bằng dấu hai chấm (:).",
                    "D. 256 bit, viết bằng hệ thập lục phân chia làm 16 nhóm."
                ],
                "answer": 2,
                "trap": "Học sinh hay nhớ nhầm giữa 32 bit (IPv4) và 64 bit hoặc 128 bit (IPv6), và nhầm dấu phân cách giữa dấu chấm (.) và dấu hai chấm (:).",
                "explanation": "IPv6 ra đời để giải quyết cạn kiệt IPv4, có độ dài 128 bit (cung cấp 2^128 địa chỉ), viết bằng các chữ số hexa (0-9, A-F) chia thành 8 nhóm cách nhau bởi dấu hai chấm (:)."
            },
            {
                "id": 11,
                "question": "Phát biểu nào sau đây là SAI về mô hình mạng ngang hàng (Peer-to-Peer - P2P)?",
                "options": [
                    "A. Mỗi máy tính trong mạng P2P vừa có thể đóng vai trò máy khách (client), vừa có thể là máy chủ (server).",
                    "B. Dữ liệu trong mạng P2P được tập trung quản lý trên một máy chủ chuyên dụng duy nhất.",
                    "C. Mạng P2P dễ triển khai, chi phí thấp cho các mạng văn phòng quy mô nhỏ.",
                    "D. Khi số lượng máy tính tăng lên nhiều, việc bảo mật và quản lý tài nguyên trong mạng P2P trở nên khó khăn."
                ],
                "answer": 1,
                "trap": "Đề bài yêu cầu tìm phát biểu SAI. Khái niệm 'dữ liệu tập trung trên một máy chủ duy nhất' là đặc trưng của mô hình Khách - Chủ (Client - Server), chứ không phải P2P.",
                "explanation": "Trong mô hình mạng ngang hàng P2P, không có máy chủ trung tâm nào. Tất cả các máy bình đẳng, tự chia sẻ tài nguyên và dữ liệu phân tán trực tiếp với nhau."
            },
            {
                "id": 12,
                "question": "Thiết bị Access Point (AP) trong mạng gia đình đóng vai trò chủ yếu là gì?",
                "options": [
                    "A. Biến đổi tín hiệu quang từ cáp của nhà mạng thành tín hiệu điện số.",
                    "B. Thu và phát sóng không dây (Wi-Fi) để các thiết bị di động kết nối vào mạng có dây cục bộ.",
                    "C. Lưu trữ toàn bộ các website mà người dùng đã từng truy cập để tăng tốc độ lướt web.",
                    "D. Ngăn chặn 100% các cuộc tấn công mạng từ bên ngoài Internet vào máy tính."
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm Access Point (điểm truy cập không dây) với Modem (bộ điều chế giải điều chế tín hiệu từ nhà mạng).",
                "explanation": "Access Point (AP) nhận tín hiệu mạng từ cáp Ethernet và phát ra sóng Wi-Fi cho điện thoại, laptop kết nối vào mạng LAN nội bộ."
            },
            {
                "id": 13,
                "question": "Khái niệm 'Băng thông' (Bandwidth) của một đường truyền Internet phản ánh điều gì?",
                "options": [
                    "A. Thời gian cần thiết để một gói tin đi từ nguồn đến đích.",
                    "B. Lượng dữ liệu tối đa có thể truyền tải qua đường truyền trong một đơn vị thời gian (thường tính bằng Mbps hoặc Gbps).",
                    "C. Chiều dài vật lý tính bằng mét của sợi cáp mạng nối từ nhà đến trạm viễn thông.",
                    "D. Số lượng thiết bị tối đa được phép cắm vào một modem mạng."
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm Băng thông (Bandwidth - độ rộng đường ống) với Độ trễ (Latency/Ping - thời gian di chuyển của giọt nước).",
                "explanation": "Băng thông (Bandwidth) là dung lượng truyền dẫn tối đa của kênh truyền trong 1 giây, đơn vị đo là bit/giây (bps), Mbps, Gbps. Độ trễ (Latency) mới là thời gian đi từ nguồn tới đích."
            },
            {
                "id": 14,
                "question": "Địa chỉ MAC (Media Access Control) của card mạng có đặc điểm nào sau đây?",
                "options": [
                    "A. Là địa chỉ logic do nhà mạng ISP tự động thay đổi mỗi lần khởi động lại modem.",
                    "B. Là địa chỉ vật lý duy nhất được nhà sản xuất ghi cố định vào phần cứng card mạng, gồm 48 bit (6 byte).",
                    "C. Là địa chỉ dùng để định tuyến gói tin vượt qua nhiều router trên phạm vi toàn cầu.",
                    "D. Chỉ máy tính dùng hệ điều hành Windows mới có địa chỉ MAC, điện thoại không có."
                ],
                "answer": 1,
                "trap": "Học sinh thường nhầm địa chỉ IP (địa chỉ logic, thay đổi theo mạng) với địa chỉ MAC (địa chỉ vật lý cố định theo chip card mạng). Mọi thiết bị kết nối mạng (PC, điện thoại, máy in) đều có MAC.",
                "explanation": "Địa chỉ MAC là địa chỉ vật lý gồm 48 bit (thường viết dạng 6 cặp số Hex: 00:1A:2B:3C:4D:5E), gán cố định từ nhà sản xuất cho chip giao tiếp mạng."
            },
            {
                "id": 15,
                "question": "Lệnh dòng lệnh nào sau đây thường được sử dụng trên Windows để kiểm tra kết nối mạng và đo thời gian phản hồi (độ trễ) tới một máy chủ?",
                "options": [
                    "A. ipconfig",
                    "B. ping",
                    "C. mkdir",
                    "D. cls"
                ],
                "answer": 1,
                "trap": "ipconfig là lệnh để XEM địa chỉ IP của máy, còn ping mới là lệnh để KIỂM TRA kết nối và đo độ trễ gói tin.",
                "explanation": "Lệnh `ping <địa chỉ IP hoặc tên miền>` gửi các gói tin ICMP Echo Request và đo thời gian (ms) nhận phản hồi để xác định kết nối mạng có thông suốt hay không."
            },
            {
                "id": 16,
                "question": "Một mạng máy tính kết nối các thiết bị trong phạm vi một phòng học, một tòa nhà hoặc một trường học được gọi là mạng gì?",
                "options": [
                    "A. Mạng diện rộng (WAN - Wide Area Network)",
                    "B. Mạng cục bộ (LAN - Local Area Network)",
                    "C. Mạng đô thị (MAN - Metropolitan Area Network)",
                    "D. Mạng toàn cầu (GAN - Global Area Network)"
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm lẫn quy mô: PAN (cá nhân vài mét) -> LAN (tòa nhà, trường học vài trăm mét) -> MAN (thành phố vài chục km) -> WAN (quốc gia, toàn cầu).",
                "explanation": "LAN (Local Area Network) là mạng cục bộ kết nối các thiết bị trong phạm vi địa lý hẹp như văn phòng, tòa nhà, trường học."
            },
            {
                "id": 17,
                "question": "Điện toán đám mây (Cloud Computing) mang lại lợi ích cốt lõi nào sau đây cho người dùng và doanh nghiệp?",
                "options": [
                    "A. Bắt buộc người dùng phải tự mua máy chủ vật lý đặt tại văn phòng.",
                    "B. Truy cập tài nguyên tính toán (lưu trữ, phần mềm, máy chủ) qua mạng theo nhu cầu mà không cần đầu tư phần cứng đắt tiền tại chỗ.",
                    "C. Đảm bảo máy tính của người dùng không bao giờ cần kết nối mạng Internet vẫn dùng được dữ liệu đám mây.",
                    "D. Thay thế hoàn toàn màn hình và bàn phím máy tính truyền thống."
                ],
                "answer": 1,
                "trap": "Học sinh chọn nhầm phương án C vì nghĩ 'đám mây là phép màu'. Để dùng điện toán đám mây thì BẮT BUỘC phải có kết nối Internet.",
                "explanation": "Điện toán đám mây cung cấp các tài nguyên công nghệ thông tin (máy chủ, dung lượng ổ đĩa, cơ sở dữ liệu) qua Internet theo mô hình trả phí theo mức sử dụng, giúp linh hoạt và tiết kiệm chi phí."
            },
            {
                "id": 18,
                "question": "Tập hợp các quy tắc chuẩn hóa nhằm đảm bảo các thiết bị khác nhau có thể hiểu và trao đổi thông tin được với nhau trên mạng được gọi là gì?",
                "options": [
                    "A. Hệ điều hành mạng (Network OS)",
                    "B. Giao thức mạng (Network Protocol)",
                    "C. Dây cáp mạng (Network Cable)",
                    "D. Phần mềm diệt virus (Antivirus)"
                ],
                "answer": 1,
                "trap": "Đây là câu hỏi định nghĩa căn bản trong SGK nhưng học sinh hay chọn nhầm Hệ điều hành mạng.",
                "explanation": "Giao thức mạng (Protocol) là tập hợp các quy tắc, thủ tục và cú pháp đã thống nhất để các máy tính (dù khác hãng sản xuất, khác hệ điều hành) vẫn giao tiếp được với nhau."
            },
            {
                "id": 19,
                "question": "Hiện tượng mạng bị 'nghẽn cổ chai' (bottleneck) tại một thiết bị Switch hoặc Router thường xảy ra khi nào?",
                "options": [
                    "A. Khi cáp mạng cắm vào thiết bị có màu sắc khác nhau.",
                    "B. Khi lưu lượng dữ liệu truyền qua thiết bị vượt quá khả năng xử lý hoặc băng thông tối đa của cổng kết nối.",
                    "C. Khi trong mạng có một máy tính cài đặt hệ điều hành Linux.",
                    "D. Khi máy tính người dùng tắt màn hình nhưng vẫn bật case."
                ],
                "answer": 1,
                "trap": "Các phương án gây nhiễu hài hước nhưng đề thi thật thường dùng từ ngữ khoa học để lừa học sinh không nắm bản chất vật lý của băng thông mạng.",
                "explanation": "Nghẽn cổ chai xảy ra khi lượng gói tin đến một nút mạng nhanh hơn tốc độ nút đó có thể xử lý hoặc đẩy tiếp, khiến hàng đợi bị đầy và các gói tin bị đánh rơi (packet loss)."
            },
            {
                "id": 20,
                "question": "Mô hình mạng Client - Server hoạt động theo nguyên lý nào sau đây?",
                "options": [
                    "A. Máy khách (Client) gửi yêu cầu (Request), máy chủ (Server) tiếp nhận, xử lý và gửi phản hồi (Response) về cho khách.",
                    "B. Máy chủ liên tục phát tán toàn bộ dữ liệu ra mạng cho mọi máy tính mà không cần máy nào yêu cầu.",
                    "C. Hai máy tính bất kỳ tự động đổi quyền điều khiển cho nhau theo chu kỳ từng giây.",
                    "D. Máy khách bắt buộc phải chứa toàn bộ mã nguồn của hệ điều hành máy chủ mới hoạt động được."
                ],
                "answer": 0,
                "trap": "Nhiều học sinh nhầm chiều tương tác: Luôn luôn là CLIENT GỬI YÊU CẦU TRƯỚC, rồi Server mới phản hồi.",
                "explanation": "Mô hình Khách - Chủ (Client-Server) hoạt động theo cơ chế Request - Response: Client gửi truy vấn (như gõ web URL), Server xử lý và trả về dữ liệu (mã HTML/dữ liệu API)."
            }
        ]
    },

    # =========================================================================
    # CHUYÊN ĐỀ 2: TRÍ TUỆ NHÂN TẠO (AI) VÀ HỌC MÁY (20 CÂU)
    # =========================================================================
    "2": {
        "topic_id": "2",
        "topic_title": "Chuyên đề 2: Trí tuệ nhân tạo (AI) và Học máy",
        "description": "20 câu trắc nghiệm cập nhật theo chương trình GDPT 2018: Phân loại AI, học có/không giám sát, mạng nơ-ron, AI tạo sinh, hiện tượng ảo giác, đạo đức và bẫy đề thi hay gặp.",
        "questions": [
            {
                "id": 1,
                "question": "Phát biểu nào sau đây phản ánh ĐÚNG thực trạng năng lực của Trí tuệ nhân tạo (AI) hiện nay?",
                "options": [
                    "A. AI hiện nay đã đạt tới mức có ý thức, cảm xúc và khả năng tư duy độc lập hệt như con người.",
                    "B. Toàn bộ các hệ thống AI hiện nay (như ChatGPT, xe tự hành, nhận diện khuôn mặt) đều thuộc loại AI hẹp (Narrow AI), chỉ giải quyết được tác vụ cụ thể.",
                    "C. AI tổng quát (AGI) đã được áp dụng phổ biến trong tất cả các bệnh viện và trường học.",
                    "D. AI có khả năng tự sáng tạo kiến thức mới mà hoàn toàn không cần dựa trên bất kỳ dữ liệu huấn luyện nào."
                ],
                "answer": 1,
                "trap": "⚠️ BẪY ĐỀ THI ĐÚNG/SAI PHẦN II: Đề hay cho mệnh đề 'AI đã có cảm xúc và nhận thức'. Mệnh đề này là SAI 100%. Mọi AI hiện nay chỉ là thuật toán toán học mô phỏng hành vi dựa trên xác suất, hoàn toàn không có ý thức.",
                "explanation": "Toàn bộ AI thực tế hiện tại là AI hẹp (Narrow AI hay Weak AI). AI tổng quát (AGI) có trí tuệ toàn diện như con người vẫn chỉ đang ở mức độ nghiên cứu lý thuyết."
            },
            {
                "id": 2,
                "question": "Sắp xếp nào sau đây thể hiện đúng mối quan hệ bao hàm (tập mẹ - tập con) giữa các lĩnh vực?",
                "options": [
                    "A. Học sâu (Deep Learning) ⊃ Học máy (Machine Learning) ⊃ Trí tuệ nhân tạo (AI)",
                    "B. Trí tuệ nhân tạo (AI) ⊃ Học máy (Machine Learning) ⊃ Học sâu (Deep Learning)",
                    "C. Học máy (Machine Learning) ⊃ Trí tuệ nhân tạo (AI) ⊃ Học sâu (Deep Learning)",
                    "D. Trí tuệ nhân tạo (AI) ⊃ Học sâu (Deep Learning) ⊃ Học máy (Machine Learning)"
                ],
                "answer": 1,
                "trap": "Học sinh hay bị đảo lộn thứ tự. AI là khái niệm rộng nhất (từ những năm 1950) -> Học máy (ML) là nhánh con sử dụng dữ liệu -> Học sâu (DL) là nhánh con của ML sử dụng mạng nơ-ron nhiều tầng.",
                "explanation": "AI là tập cha lớn nhất. Machine Learning là một phân nhánh của AI. Deep Learning lại là một phân nhánh chuyên sâu của Machine Learning dựa trên mạng nơ-ron nhân tạo sâu."
            },
            {
                "id": 3,
                "question": "Một hệ thống AI được cung cấp 10.000 bức ảnh, trong đó mỗi bức ảnh đều ĐÃ ĐƯỢC GẮN NHÃN sẵn là 'Chó' hoặc 'Mèo' để máy học cách phân loại. Đây là phương pháp học máy nào?",
                "options": [
                    "A. Học không giám sát (Unsupervised Learning)",
                    "B. Học có giám sát (Supervised Learning)",
                    "C. Học tăng cường (Reinforcement Learning)",
                    "D. Học ngẫu nhiên (Random Learning)"
                ],
                "answer": 1,
                "trap": "Từ khóa quyết định là 'ĐÃ ĐƯỢC GẮN NHÃN' (labeled data). Có nhãn -> Giám sát. Không có nhãn -> Không giám sát.",
                "explanation": "Học có giám sát (Supervised Learning) là phương pháp huấn luyện mô hình dựa trên tập dữ liệu đã có cả đầu vào (ảnh) và nhãn kết quả mong muốn (chó/mèo)."
            },
            {
                "id": 4,
                "question": "Một trang thương mại điện tử sử dụng AI để tự động phân tích hành vi của hàng triệu khách hàng và tự gom họ thành các nhóm có sở thích tương tự nhau mà KHÔNG hề có nhãn định trước. Đây là ví dụ của:",
                "options": [
                    "A. Học có giám sát (Supervised Learning)",
                    "B. Học không giám sát (Unsupervised Learning)",
                    "C. Lập trình thủ công bằng câu lệnh if-else",
                    "D. Học tăng cường (Reinforcement Learning)"
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm với Học có giám sát. Ở đây hệ thống tự phân cụm (Clustering) từ dữ liệu thô chưa hề được con người dán nhãn phân loại từ trước.",
                "explanation": "Học không giám sát (Unsupervised Learning) tự động tìm kiếm các quy luật, mẫu hình hoặc phân cụm (clustering) từ tập dữ liệu đầu vào mà không cần nhãn đích."
            },
            {
                "id": 5,
                "question": "Hiện tượng 'Ảo giác' (Hallucination) trong các mô hình ngôn ngữ lớn (như ChatGPT) được hiểu là gì?",
                "options": [
                    "A. Màn hình máy tính của người dùng bị nhấp nháy liên tục khi sử dụng AI.",
                    "B. Mô hình AI tự nhận thức được nó là một con người và từ chối trả lời câu hỏi.",
                    "C. Mô hình AI tự tin tạo ra các thông tin hoàn toàn sai sự thật hoặc trích dẫn nguồn không có thật nhưng văn phong rất lưu loát, thuyết phục.",
                    "D. AI bị nhiễm virus mã hóa tống tiền khiến câu trả lời bị biến thành ký tự lạ."
                ],
                "answer": 2,
                "trap": "Nhiều người lầm tưởng ChatGPT luôn luôn nói đúng hoặc nếu sai thì nó sẽ báo lỗi. Thực tế nó dự đoán từ tiếp theo theo xác suất, nên có thể 'chém gió' tạo ra thông tin giả mạo rất mượt mà.",
                "explanation": "Ảo giác (Hallucination) là hiện tượng mô hình AI sinh tạo ra thông tin không chính xác về mặt thực tế hoặc trích dẫn các bài báo/tác giả không hề tồn tại nhưng trình bày rất mạch lạc."
            },
            {
                "id": 6,
                "question": "Trong học máy, hiện tượng 'Quá khớp' (Overfitting) xảy ra khi nào?",
                "options": [
                    "A. Mô hình học quá kém trên cả tập dữ liệu huấn luyện lẫn tập dữ liệu kiểm tra.",
                    "B. Mô hình học quá kỹ và 'học vẹt' từng chi tiết của tập huấn luyện, dẫn đến kết quả xuất sắc trên dữ liệu cũ nhưng dự đoán rất kém trên dữ liệu mới.",
                    "C. Mô hình hoàn thành việc học chỉ sau 1 giây mà không cần tính toán.",
                    "D. Dữ liệu huấn luyện bị mất hoàn toàn do lỗi phần cứng máy chủ."
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm Overfitting với việc 'mô hình hoạt động hoàn hảo'. Thực chất Overfitting giống như học sinh học tủ học vẹt đề cương cũ, đổi số một chút trong đề thi thật là làm sai ngay.",
                "explanation": "Overfitting xảy ra khi mô hình quá phức tạp, ghi nhớ cả các nhiễu trong tập train, mất khả năng khái quát hóa (generalization) trên dữ liệu thực tế mới."
            },
            {
                "id": 7,
                "question": "Hệ thống AI AlphaGo học cách chơi cờ vây bằng cách chơi hàng triệu ván cờ với chính nó và nhận điểm thưởng khi thắng, điểm phạt khi thua. Phương pháp này thuộc loại:",
                "options": [
                    "A. Học tăng cường (Reinforcement Learning)",
                    "B. Học có giám sát (Supervised Learning)",
                    "C. Học không giám sát (Unsupervised Learning)",
                    "D. Lập trình tuần tự truyền thống"
                ],
                "answer": 0,
                "trap": "Từ khóa cốt lõi: 'Hành động trong môi trường' và 'Điểm thưởng / Điểm phạt' (Reward/Penalty) chính là bản chất của Học tăng cường.",
                "explanation": "Học tăng cường (Reinforcement Learning) đào tạo tác tử (Agent) thông qua thử và sai để tối đa hóa phần thưởng tích lũy trong môi trường."
            },
            {
                "id": 8,
                "question": "Một mô hình AI tuyển dụng nhân sự tự động ưu tiên ứng viên nam hơn ứng viên nữ dù cùng trình độ. Nguyên nhân cốt lõi của sự 'thiên vị' (AI Bias) này là do:",
                "options": [
                    "A. Bản thân máy tính có tư tưởng phân biệt đối xử bẩm sinh.",
                    "B. Dữ liệu lịch sử tuyển dụng trong quá khứ dùng để huấn luyện AI đã mang sẵn sự mất cân bằng và định kiến của con người.",
                    "C. Tốc độ xung nhịp của CPU máy chủ chạy AI quá cao.",
                    "D. Các thuật toán học máy chỉ hoạt động được trên dữ liệu của nam giới."
                ],
                "answer": 1,
                "trap": "Học sinh thường nghĩ 'AI tự nảy sinh ác ý'. Nhưng nguyên nhân thực sự 100% nằm ở DỮ LIỆU HUẤN LUYỆN bị lệch mà con người đưa vào (Garbage in, Garbage out).",
                "explanation": "Định kiến trong AI (AI Bias) bắt nguồn từ việc tập dữ liệu huấn luyện thu thập từ quá khứ phản ánh sự bất bình đẳng hoặc thiếu mẫu đại diện công bằng của xã hội loài người."
            },
            {
                "id": 9,
                "question": "Phép thử Turing (Turing Test) do nhà toán học Alan Turing đề xuất nhằm mục đích gì?",
                "options": [
                    "A. Kiểm tra xem một cỗ máy tính toán có chạy nhanh hơn bộ vi xử lý Intel Core i9 không.",
                    "B. Kiểm tra xem hành vi giao tiếp của một cỗ máy có thông minh đến mức khiến con người không thể phân biệt được là máy hay người hay không.",
                    "C. Kiểm tra xem máy tính có bị nhiễm virus hay mã độc hay không.",
                    "D. Kiểm tra xem máy móc đã có linh hồn và cảm xúc chưa."
                ],
                "answer": 1,
                "trap": "Phép thử Turing không đo tốc độ CPU, cũng không đo cảm xúc/linh hồn, mà chỉ đo KHẢ NĂNG THỂ HIỆN HÀNH VI THÔNG MINH trong đối thoại qua văn bản.",
                "explanation": "Phép thử Turing xác định máy có hành vi trí tuệ tương đương con người nếu một người đánh giá mù (chỉ trò chuyện qua chữ) không thể phân biệt đối phương là máy hay người thật."
            },
            {
                "id": 10,
                "question": "Thuật toán Thị giác máy tính (Computer Vision) ứng dụng trong đời sống thực tế vào tác vụ nào sau đây?",
                "options": [
                    "A. Dịch tự động một văn bản từ tiếng Anh sang tiếng Việt.",
                    "B. Nhận diện biển số xe vi phạm giao thông và mở khóa điện thoại bằng khuôn mặt (FaceID).",
                    "C. Soạn thảo hợp đồng pháp lý tự động bằng văn bản.",
                    "D. Nén file dữ liệu định dạng ZIP."
                ],
                "answer": 1,
                "trap": "Dịch văn bản là Xử lý ngôn ngữ tự nhiên (NLP). Nhận diện biển số và FaceID liên quan đến hình ảnh/video nên thuộc Thị giác máy tính (Computer Vision).",
                "explanation": "Thị giác máy tính (Computer Vision) nghiên cứu giúp máy tính có khả năng 'nhìn' và hiểu nội dung từ hình ảnh, video số (nhận dạng vật thể, khuôn mặt, biển số)."
            },
            {
                "id": 11,
                "question": "Khái niệm 'Mạng nơ-ron nhân tạo' (Artificial Neural Network - ANN) được lấy cảm hứng từ cấu trúc nào?",
                "options": [
                    "A. Hệ thống mạch điện bán dẫn bên trong transistor.",
                    "B. Cấu trúc mạng lưới nơ-ron và các khớp nối sinap trong hệ thần kinh sinh học của não bộ con người.",
                    "C. Sơ đồ phân nhánh của cây phả hệ gia đình.",
                    "D. Mô hình kết nối dây cáp quang ngầm dưới đáy biển."
                ],
                "answer": 1,
                "trap": "Học sinh học môn Tin học đôi khi quên liên hệ kiến thức Sinh học. Mạng nơ-ron nhân tạo mô phỏng tế bào thần kinh sinh học (Neuron).",
                "explanation": "ANN là mô hình xử lý thông tin toán học mô phỏng theo mạng lưới tế bào thần kinh sinh học, gồm các tầng node (nơ-ron) kết nối với nhau qua các trọng số (weights)."
            },
            {
                "id": 12,
                "question": "Công nghệ nào dưới đây thuộc phân nhánh Trí tuệ nhân tạo tạo sinh (Generative AI)?",
                "options": [
                    "A. Máy tính cầm tay Casio bấm giải phương trình bậc hai.",
                    "B. Mô hình Midjourney vẽ tranh theo mô tả văn bản (Text-to-Image) và ChatGPT viết bài luận.",
                    "C. Thiết bị đo nhiệt độ nước sôi hiển thị số.",
                    "D. Phần mềm diệt virus quét file theo chữ ký mã độc có sẵn."
                ],
                "answer": 1,
                "trap": "Generative AI là AI có khả năng TẠO RA NỘI DUNG MỚI (chữ, ảnh, âm thanh, video, code), không chỉ đơn thuần là phân loại hay tính toán công thức cố định.",
                "explanation": "Generative AI (AI sinh tạo) sử dụng các mô hình học sâu để sáng tạo ra dữ liệu mới (văn bản, tranh vẽ, âm nhạc, video) có độ phức tạp cao tương tự tác phẩm con người tạo ra."
            },
            {
                "id": 13,
                "question": "Hành vi nào sau đây là vi phạm đạo đức và quy định pháp luật khi sử dụng công nghệ AI?",
                "options": [
                    "A. Sử dụng AI để gợi ý tìm kiếm tài liệu học tập và tham khảo ý tưởng.",
                    "B. Dùng công nghệ Deepfake giả mạo hình ảnh, giọng nói của người khác để lừa đảo chiếm đoạt tài sản hoặc bôi nhọ danh dự.",
                    "C. Nhờ AI giải thích giúp một lỗi sai trong đoạn code lập trình Python.",
                    "D. Dùng AI kiểm tra lỗi chính tả trong bài tiểu luận cá nhân."
                ],
                "answer": 1,
                "trap": "Câu hỏi đạo đức công nghệ: Deepfake giả mạo hình ảnh/âm thanh người khác khi không được phép là hành vi vi phạm nghiêm trọng cả pháp luật lẫn đạo đức.",
                "explanation": "Sử dụng Deepfake để mạo danh, bôi nhọ, tống tiền hoặc lừa đảo vi phạm nghiêm trọng Luật An ninh mạng và các quy định pháp luật về bảo vệ quyền nhân thân."
            },
            {
                "id": 14,
                "question": "Trong xử lý ngôn ngữ tự nhiên (NLP), tác vụ 'Phân tích cảm xúc' (Sentiment Analysis) thường được dùng để làm gì?",
                "options": [
                    "A. Đếm số từ có trong một trang sách.",
                    "B. Xác định ý kiến, thái độ của người viết (Tích cực, Tiêu cực hay Trung tính) qua các bình luận đánh giá sản phẩm.",
                    "C. Kiểm tra xem bàn phím máy tính đang gõ bằng tiếng Anh hay tiếng Việt.",
                    "D. Thay đổi font chữ của đoạn văn bản cho đẹp mắt."
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm với kiểm tra chính tả. Sentiment Analysis là phân loại trạng thái cảm xúc (khen/chê) của khách hàng.",
                "explanation": "Phân tích cảm xúc (Sentiment Analysis) phân loại quan điểm, sắc thái cảm xúc của văn bản (tích cực, tiêu cực, trung tính) dựa trên ngữ nghĩa từ ngữ."
            },
            {
                "id": 15,
                "question": "Khái niệm 'Dữ liệu lớn' (Big Data) thường được đặc trưng bởi mô hình '4V'. '4V' đại diện cho những yếu tố nào?",
                "options": [
                    "A. Volume (Dung lượng lớn), Velocity (Tốc độ nhanh), Variety (Đa dạng dạng dữ liệu), Veracity (Độ chính xác/tin cậy).",
                    "B. Video, Voice, Virus, Virtual.",
                    "C. Value, View, Version, Vector.",
                    "D. Voltage, Viber, Vulnerability, Variable."
                ],
                "answer": 0,
                "trap": "Đề thi hay đưa ra các từ bắt đầu bằng chữ V nghe rất quen thuộc để bẫy học sinh không học kỹ định nghĩa 4V của Big Data.",
                "explanation": "4V kinh điển của Big Data bao gồm: Volume (khối lượng cực lớn), Velocity (tốc độ phát sinh và xử lý liên tục), Variety (nhiều định dạng: chữ, ảnh, video, log), Veracity (tính xác thực, chất lượng dữ liệu)."
            },
            {
                "id": 16,
                "question": "Một ứng dụng bản đồ như Google Maps tính toán lộ trình đường đi ngắn nhất và tránh điểm tắc đường trong thời gian thực chủ yếu ứng dụng thành phần nào?",
                "options": [
                    "A. Nhận diện chữ viết tay qua camera.",
                    "B. Thuật toán tìm đường tối ưu trên đồ thị kết hợp dữ liệu lớn về mật độ phương tiện theo thời gian thực.",
                    "C. Công nghệ nén file MP3.",
                    "D. Thuật toán mã hóa khóa công khai RSA."
                ],
                "answer": 1,
                "trap": "Học sinh cần nắm bản chất: bản đồ mạng lưới đường xá là cấu trúc Đồ thị (Graph), kết hợp AI phân tích luồng dữ liệu GPS từ hàng triệu điện thoại trên đường.",
                "explanation": "Google Maps áp dụng thuật toán tìm đường trên đồ thị (như Dijkstra/A*) kết hợp AI dự đoán lưu lượng xe cộ dựa trên dữ liệu vị trí theo thời gian thực."
            },
            {
                "id": 17,
                "question": "Tại sao việc đưa dữ liệu huấn luyện có số lượng quá ít vào mô hình Học sâu (Deep Learning) lại không đem lại hiệu quả cao?",
                "options": [
                    "A. Vì mô hình Deep Learning có hàng triệu đến hàng tỷ tham số, cần lượng dữ liệu khổng lồ để hội tụ và khái quát hóa chính xác.",
                    "B. Vì máy tính sẽ tự động từ chối chạy nếu tập dữ liệu dưới 1 GB.",
                    "C. Vì thuật toán Deep Learning chỉ chấp nhận dữ liệu dạng video, không chấp nhận dạng bảng.",
                    "D. Vì Deep Learning không sử dụng phép tính số học nào."
                ],
                "answer": 0,
                "trap": "Nếu ít dữ liệu, các thuật toán học máy truyền thống (như SVM, Decision Tree) thường chạy tốt hơn Deep Learning. Deep Learning chỉ phát huy sức mạnh vượt trội khi có Dữ liệu lớn (Big Data).",
                "explanation": "Mạng nơ-ron sâu chứa rất nhiều tầng ẩn và hàng triệu trọng số, nếu ít dữ liệu sẽ dẫn tới hiện tượng Underfitting hoặc Overfitting trầm trọng."
            },
            {
                "id": 18,
                "question": "Hệ thống khuyến nghị (Recommendation System) trên các nền tảng như YouTube, TikTok hoặc Shopee hoạt động dựa trên nguyên lý nào?",
                "options": [
                    "A. Luôn luôn chiếu ngẫu nhiên các video mới tải lên mà không theo quy luật nào.",
                    "B. Thu thập lịch sử xem, tương tác, thời gian dừng và sở thích của người dùng để đề xuất các nội dung có xác suất người đó yêu thích cao nhất.",
                    "C. Bắt buộc người dùng phải gõ tìm kiếm thủ công từng video một.",
                    "D. Chỉ gợi ý video của các tài khoản có cùng họ tên với người dùng."
                ],
                "answer": 1,
                "trap": "Nhiều người nghĩ thuật toán gợi ý là 'ngẫu nhiên'. Thực chất đó là mô hình Học máy lọc cộng tác (Collaborative Filtering) phân tích hành vi người dùng cực kỳ chi tiết.",
                "explanation": "Hệ thống khuyến nghị sử dụng học máy phân tích hành vi quá khứ và sự tương đồng giữa các người dùng để đưa ra nội dung được cá nhân hóa cao nhất."
            },
            {
                "id": 19,
                "question": "Phát biểu nào sau đây là ĐÚNG về bản quyền tác phẩm do AI tự động tạo ra?",
                "options": [
                    "A. Theo luật pháp hiện hành tại hầu hết các quốc gia, bản thân cỗ máy AI không phải là con người nên không được công nhận là tác giả nắm giữ quyền tác giả.",
                    "B. AI tự động được cấp bằng sáng chế và nhận tiền tác quyền vào tài khoản ngân hàng riêng của máy tính.",
                    "C. Bất kỳ ai dùng AI tạo ra ảnh đều đương nhiên sở hữu bản quyền vô điều kiện mà không cần xét đến dữ liệu nguồn.",
                    "D. Tác phẩm do AI vẽ không bao giờ có thể tranh chấp bản quyền với tranh của họa sĩ thật."
                ],
                "answer": 0,
                "trap": "⚠️ BẪY PHÁP LÝ: Pháp luật chỉ công nhận QUYỀN TÁC GIẢ cho CON NGƯỜI (sáng tạo trí tuệ của cá nhân). Máy móc, robot không có tư cách pháp nhân nên không thể đứng tên tác giả.",
                "explanation": "Pháp luật sở hữu trí tuệ hiện nay xác định chủ thể quyền tác giả phải là con người sáng tạo trực tiếp. Máy móc hoặc phần mềm AI chỉ là công cụ hỗ trợ."
            },
            {
                "id": 20,
                "question": "Tác vụ nào sau đây con người hiện nay vẫn vượt trội hoàn toàn so với mọi hệ thống AI hiện đại nhất?",
                "options": [
                    "A. Khả năng tính nhẩm căn bậc hai của một số có 50 chữ số trong 1 mili-giây.",
                    "B. Khả năng thấu cảm, hiểu biết xã hội sâu sắc, đạo đức, lương tâm và tư duy phản biện dựa trên bối cảnh phức tạp.",
                    "C. Khả năng lưu trữ hàng triệu cuốn sách và trích dẫn tức thì.",
                    "D. Khả năng chơi cờ vua với hàng nghìn thế cờ trong 1 giây mà không mệt mỏi."
                ],
                "answer": 1,
                "trap": "Học sinh thường bị choáng ngợp bởi khả năng tính toán của AI mà quên mất các phẩm chất đặc trưng của nhân loại: Lương tâm, Thấu cảm (Empathy), Sáng tạo có chủ đích và Trách nhiệm đạo đức.",
                "explanation": "AI chỉ giỏi tính toán số học và khớp mẫu theo xác suất dữ liệu. Con người vượt trội ở tư duy trực giác, cảm xúc, thấu cảm, ý thức đạo đức và khả năng thích nghi với các bối cảnh xã hội linh hoạt."
            }
        ]
    },

    # =========================================================================
    # CHUYÊN ĐỀ 3: CƠ SỞ DỮ LIỆU (CSDL) VÀ SQL (20 CÂU)
    # =========================================================================
    "3": {
        "topic_id": "3",
        "topic_title": "Chuyên đề 3: Cơ sở dữ liệu (CSDL) và SQL",
        "description": "20 câu trắc nghiệm then chốt: Mô hình quan hệ, khóa chính, khóa ngoài, bẫy NULL, các hàm tổng hợp COUNT/SUM/AVG, mệnh đề WHERE vs HAVING, phép JOIN và toàn vẹn dữ liệu.",
        "questions": [
            {
                "id": 1,
                "question": "Đặc điểm nào sau đây là BẮT BUỘC đối với một Khóa chính (Primary Key) trong bảng CSDL quan hệ?",
                "options": [
                    "A. Có thể chứa giá trị trùng lặp giữa các dòng nhưng không được rỗng.",
                    "B. Bắt buộc phải mang giá trị DUY NHẤT và KHÔNG ĐƯỢC PHÉP CHỨA GIÁ TRỊ NULL.",
                    "C. Phải có kiểu dữ liệu là số nguyên (INTEGER), không được là kiểu chuỗi.",
                    "D. Bắt buộc phải là cột đầu tiên nằm ngoài cùng bên trái của bảng."
                ],
                "answer": 1,
                "trap": "Học sinh hay nghĩ khóa chính bắt buộc phải là số (Auto-increment). Thực tế khóa chính có thể là chuỗi ký tự (như CCCD, MaHS, MaSP), nhưng tiên quyết phải DUY NHẤT và KHÔNG NULL (Not Null).",
                "explanation": "Khóa chính (Primary Key) định danh duy nhất cho từng bản ghi trong bảng. Hai quy tắc bất di bất dịch của khóa chính là: Tính duy nhất (Unique) và Tính toàn vẹn thực thể (Không được chứa giá trị NULL)."
            },
            {
                "id": 2,
                "question": "Phát biểu nào sau đây về Khóa ngoài (Foreign Key) là ĐÚNG?",
                "options": [
                    "A. Khóa ngoài bắt buộc phải mang giá trị duy nhất trong bảng chứa nó.",
                    "B. Khóa ngoài dùng để liên kết với Khóa chính của bảng khác, và có thể chứa giá trị NULL (nếu không có ràng buộc NOT NULL).",
                    "C. Một bảng chỉ được phép có tối đa một khóa ngoài duy nhất.",
                    "D. Tên của cột khóa ngoài bắt buộc phải viết giống 100% từng chữ cái với tên cột khóa chính được tham chiếu."
                ],
                "answer": 1,
                "trap": "Rất nhiều bạn tưởng khóa ngoài cũng phải Unique và Not Null như khóa chính. Thực tế nhiều học sinh có thể cùng thuộc một MaLop (trùng lặp bình thường), và học sinh mới chuyển trường có thể tạm thời chưa xếp lớp (mang giá trị NULL).",
                "explanation": "Khóa ngoài (Foreign Key) thiết lập mối quan hệ giữa 2 bảng. Giá trị của khóa ngoài phải xuất hiện ở khóa chính của bảng tham chiếu hoặc mang giá trị NULL."
            },
            {
                "id": 3,
                "question": "Cho bảng `NHAN_VIEN` có 10 dòng, trong đó cột `HoaHong` có 3 dòng mang giá trị NULL, 7 dòng mang các giá trị số. Kết quả của câu lệnh `SELECT COUNT(HoaHong) FROM NHAN_VIEN;` là bao nhiêu?",
                "options": [
                    "A. 10",
                    "B. 7",
                    "C. 3",
                    "D. Báo lỗi vì cột có giá trị NULL không thể đếm được"
                ],
                "answer": 1,
                "trap": "⚠️ BẪY KINH ĐIỂN CỦA HÀM COUNT: `COUNT(*)` đếm TOÀN BỘ các dòng (kết quả là 10). Nhưng `COUNT(tên_cột)` sẽ TỰ ĐỘNG BỎ QUA các dòng mang giá trị NULL! Do đó kết quả chỉ là 7.",
                "explanation": "Hàm tổng hợp `COUNT(ten_cot)` chỉ đếm các ô có dữ liệu thực tế và tự động loại bỏ các ô chứa giá trị NULL. Chỉ có `COUNT(*)` mới đếm mọi dòng bất kể có NULL hay không."
            },
            {
                "id": 4,
                "question": "Trong SQL, giá trị `NULL` được hiểu chính xác là gì?",
                "options": [
                    "A. Tương đương với số 0 trong toán học.",
                    "B. Tương đương với chuỗi ký tự rỗng (\"\").",
                    "C. Thể hiện trạng thái dữ liệu chưa biết, chưa xác định hoặc không áp dụng được.",
                    "D. Là một lỗi cú pháp xuất hiện khi người nhập liệu gõ sai chính tả."
                ],
                "answer": 2,
                "trap": "Học sinh hay đánh đồng NULL = 0 hoặc NULL = \"\". Điều này hoàn toàn sai. Số 0 là một giá trị số đã biết; còn NULL là chưa biết (chưa có thông tin).",
                "explanation": "NULL trong CSDL đại diện cho thông tin bị thiếu (missing value) hoặc chưa biết. Phép so sánh `cot = NULL` luôn trả về UNKNOWN; muốn kiểm tra phải dùng toán tử `IS NULL` hoặc `IS NOT NULL`."
            },
            {
                "id": 5,
                "question": "Để tìm danh sách các sinh viên có điểm trung bình bị bỏ trống (chưa có điểm) trong bảng `SINH_VIEN`, câu lệnh SQL nào sau đây là ĐÚNG?",
                "options": [
                    "A. SELECT * FROM SINH_VIEN WHERE DiemTB = NULL;",
                    "B. SELECT * FROM SINH_VIEN WHERE DiemTB IS NULL;",
                    "C. SELECT * FROM SINH_VIEN WHERE DiemTB == 'NULL';",
                    "D. SELECT * FROM SINH_VIEN WHERE DiemTB IN (NULL);"
                ],
                "answer": 1,
                "trap": "⚠️ BẪY PHỔ BIẾN NHẤT: Rất nhiều học sinh chọn `WHERE DiemTB = NULL`. Trong SQL, dấu `=` không thể dùng với NULL vì NULL không bằng bất kỳ thứ gì, kể cả chính nó! Bắt buộc phải dùng `IS NULL`.",
                "explanation": "Theo chuẩn SQL, toán tử `IS NULL` và `IS NOT NULL` là cách hợp lệ duy nhất để kiểm tra sự tồn tại của giá trị NULL."
            },
            {
                "id": 6,
                "question": "Sự khác biệt căn bản giữa mệnh đề `WHERE` và mệnh đề `HAVING` trong câu lệnh truy vấn SQL là gì?",
                "options": [
                    "A. WHERE và HAVING có chức năng y hệt nhau, viết từ nào trước cũng được.",
                    "B. WHERE lọc dữ liệu trên từng dòng trước khi nhóm; HAVING lọc kết quả của các nhóm sau khi đã gom nhóm bằng GROUP BY.",
                    "C. WHERE dùng cho các phép toán số học, HAVING chỉ dùng cho chuỗi ký tự.",
                    "D. WHERE chỉ dùng được trong bảng đơn, HAVING chỉ dùng khi kết nối nhiều bảng."
                ],
                "answer": 1,
                "trap": "Học sinh hay dùng hàm tổng hợp (như `WHERE COUNT(*) > 5`), việc này lập tức gây lỗi cú pháp! Các hàm tổng hợp chỉ được phép kiểm tra điều kiện bên trong mệnh đề `HAVING`.",
                "explanation": "WHERE lọc từng bản ghi riêng lẻ trước khi nhóm và không áp dụng được cho hàm tổng hợp. HAVING lọc trên các nhóm sau mệnh đề GROUP BY và chuyên dùng với các hàm SUM, AVG, COUNT, MAX, MIN."
            },
            {
                "id": 7,
                "question": "Cho câu lệnh: `SELECT MaLop, COUNT(*) FROM HOC_SINH GROUP BY MaLop HAVING COUNT(*) >= 35;`. Câu lệnh này thực hiện công việc gì?",
                "options": [
                    "A. Đếm số học sinh có điểm thi lớn hơn hoặc bằng 35.",
                    "B. Liệt kê mã lớp và sĩ số của những lớp có từ 35 học sinh trở lên.",
                    "C. Xóa các lớp có dưới 35 học sinh ra khỏi cơ sở dữ liệu.",
                    "D. Cập nhật sĩ số lớp thành 35 cho toàn bộ học sinh."
                ],
                "answer": 1,
                "trap": "Đọc kỹ từ khóa: `GROUP BY MaLop` (nhóm theo lớp), `COUNT(*)` (đếm sĩ số), `HAVING COUNT(*) >= 35` (chỉ lấy lớp có sĩ số từ 35 trở lên).",
                "explanation": "Câu lệnh nhóm học sinh theo từng lớp, đếm số lượng học sinh trong từng nhóm và dùng HAVING để lọc chỉ hiển thị những lớp có số lượng >= 35."
            },
            {
                "id": 8,
                "question": "Khi muốn tìm các học sinh có họ là 'Nguyễn' trong cột `HoTen`, mệnh đề WHERE nào sau đây là chính xác?",
                "options": [
                    "A. WHERE HoTen LIKE 'Nguyễn%'",
                    "B. WHERE HoTen LIKE 'Nguyễn_'",
                    "C. WHERE HoTen = 'Nguyễn*'",
                    "D. WHERE HoTen IN ('Nguyễn')"
                ],
                "answer": 0,
                "trap": "Học sinh hay nhầm dấu `%` và `_`. Dấu `%` đại diện cho MỘT CHUỖI KÝ TỰ BẤT KỲ (độ dài tùy ý). Còn dấu `_` chỉ đại diện cho ĐÚNG 1 KÝ TỰ đơn lẻ.",
                "explanation": "Trong toán tử LIKE của SQL: `%` khớp với 0 hoặc nhiều ký tự bất kỳ. Do đó `'Nguyễn%'` sẽ khớp với 'Nguyễn Văn A', 'Nguyễn Thị B'..."
            },
            {
                "id": 9,
                "question": "Phép kết nối `INNER JOIN` giữa bảng A và bảng B trả về tập kết quả gồm các bản ghi nào?",
                "options": [
                    "A. Toàn bộ các dòng của bảng A và toàn bộ các dòng của bảng B bất kể có khớp hay không.",
                    "B. Chỉ những dòng thỏa mãn điều kiện kết nối (có sự trùng khớp giá trị khóa giữa hai bảng).",
                    "C. Luôn luôn trả về bảng rỗng nếu hai bảng có số lượng dòng khác nhau.",
                    "D. Toàn bộ các dòng của bảng A, các dòng không khớp của bảng B sẽ điền NULL."
                ],
                "answer": 1,
                "trap": "Phần D mô tả phép LEFT JOIN (hoặc LEFT OUTER JOIN). Còn INNER JOIN chỉ lấy phần giao (giao điểm) thỏa mãn điều kiện nối của cả hai bảng.",
                "explanation": "INNER JOIN (kết nối trong) chỉ trả về các hàng khi có ít nhất một sự khớp nối giữa các cột được chỉ định trong mệnh đề ON của cả 2 bảng."
            },
            {
                "id": 10,
                "question": "Để sắp xếp danh sách kết quả theo điểm thi từ cao xuống thấp (giảm dần), ta sử dụng từ khóa nào trong mệnh đề `ORDER BY`?",
                "options": [
                    "A. ASC",
                    "B. DESC",
                    "C. DOWN",
                    "D. TOP"
                ],
                "answer": 1,
                "trap": "ASC là viết tắt của Ascending (tăng dần - mặc định). DESC là viết tắt của Descending (giảm dần - từ cao xuống thấp).",
                "explanation": "`ORDER BY Diem DESC` sắp xếp các hàng có giá trị lớn nhất lên đầu và giảm dần xuống cuối."
            },
            {
                "id": 11,
                "question": "Để xóa toàn bộ dữ liệu của học sinh có mã `HS005` ra khỏi bảng `HOC_SINH`, câu lệnh SQL nào sau đây là ĐÚNG?",
                "options": [
                    "A. REMOVE FROM HOC_SINH WHERE MaHS = 'HS005';",
                    "B. DELETE FROM HOC_SINH WHERE MaHS = 'HS005';",
                    "C. DROP HOC_SINH WHERE MaHS = 'HS005';",
                    "D. CLEAR TABLE HOC_SINH WHERE MaHS = 'HS005';"
                ],
                "answer": 1,
                "trap": "SQL không có lệnh REMOVE hay CLEAR TABLE. Lệnh DROP dùng để xóa toàn bộ cấu trúc bảng/database. Muốn xóa bản ghi (dòng) phải dùng `DELETE FROM ... WHERE ...`.",
                "explanation": "Cú pháp chuẩn để xóa một hoặc nhiều hàng dữ liệu trong bảng là `DELETE FROM <tên_bảng> WHERE <điều_kiện>;`. Nếu không có WHERE, toàn bộ dòng trong bảng sẽ bị xóa sạch."
            },
            {
                "id": 12,
                "question": "Để thêm một bản ghi mới vào bảng `LOP(MaLop, TenLop)`, câu lệnh nào sau đây đúng cú pháp?",
                "options": [
                    "A. ADD INTO LOP VALUES ('12A1', 'Lớp 12A1');",
                    "B. INSERT INTO LOP (MaLop, TenLop) VALUES ('12A1', 'Lớp 12A1');",
                    "C. UPDATE LOP SET MaLop = '12A1', TenLop = 'Lớp 12A1';",
                    "D. CREATE ROW LOP ('12A1', 'Lớp 12A1');"
                ],
                "answer": 1,
                "trap": "Nhiều học sinh nhầm giữa lệnh INSERT INTO (thêm bản ghi mới) với lệnh UPDATE (sửa bản ghi cũ) hoặc nhầm với từ khóa ADD trong ALTER TABLE.",
                "explanation": "Cú pháp thêm dòng mới vào bảng trong SQL là: `INSERT INTO <tên_bảng> [(danh_sách_cột)] VALUES (danh_sách_giá_trị);`."
            },
            {
                "id": 13,
                "question": "Mối quan hệ Nhiều - Nhiều (N - N) giữa hai thực thể (ví dụ: một Sinh viên đăng ký nhiều Môn học, một Môn học có nhiều Sinh viên theo học) trong mô hình CSDL quan hệ được giải quyết như thế nào?",
                "options": [
                    "A. Gộp cả hai bảng thành một bảng duy nhất và lặp lại dữ liệu nhiều lần.",
                    "B. Tách thành hai mối quan hệ Một - Nhiều (1 - N) bằng cách tạo thêm một bảng trung gian (bảng nối) chứa khóa ngoại tham chiếu đến cả hai bảng.",
                    "C. Khai báo cột SinhVien chứa danh sách các môn học phân cách bằng dấu phẩy.",
                    "D. Mô hình quan hệ không thể lưu trữ mối quan hệ nhiều - nhiều."
                ],
                "answer": 1,
                "trap": "Việc lưu danh sách ngăn cách bằng dấu phẩy vi phạm dạng chuẩn 1NF (tính nguyên tố). Cách giải quyết chuẩn mực duy nhất là tạo bảng trung gian (Junction Table).",
                "explanation": "Trong thiết kế CSDL quan hệ, mối quan hệ N-N luôn được chuyển đổi thành 2 quan hệ 1-N thông qua một bảng liên kết trung gian chứa các cặp khóa ngoài tương ứng."
            },
            {
                "id": 14,
                "question": "Câu lệnh `SELECT DISTINCT QueQuan FROM SINH_VIEN;` mang lại kết quả gì?",
                "options": [
                    "A. Danh sách quê quán của tất cả sinh viên, giữ nguyên mọi sự trùng lặp.",
                    "B. Danh sách các quê quán khác nhau (đã được loại bỏ hoàn toàn các giá trị trùng lặp).",
                    "C. Đếm số lượng quê quán có trong bảng sinh viên.",
                    "D. Sắp xếp quê quán theo thứ tự bảng chữ cái ABC."
                ],
                "answer": 1,
                "trap": "Từ khóa `DISTINCT` dùng để khử trùng lặp (chỉ lấy các giá trị phân biệt). Nhiều bạn nhầm DISTINCT với hàm đếm COUNT.",
                "explanation": "Từ khóa `DISTINCT` đi sau SELECT chỉ định việc loại trừ các hàng có nội dung hoàn toàn trùng lặp trong tập kết quả trả về."
            },
            {
                "id": 15,
                "question": "Quy tắc 'Toàn vẹn tham chiếu' (Referential Integrity) sẽ ngăn chặn thao tác nào sau đây?",
                "options": [
                    "A. Thêm một học sinh mới vào một lớp học đã có sẵn trong bảng Lớp.",
                    "B. Xóa một lớp học trong bảng Lớp khi vẫn đang có các học sinh thuộc lớp đó tham chiếu tới ở bảng Học sinh.",
                    "C. Cập nhật tên của một học sinh trong bảng Học sinh.",
                    "D. Xem danh sách các học sinh có điểm trung bình trên 8.0."
                ],
                "answer": 1,
                "trap": "Nếu xóa lớp đó đi thì các học sinh thuộc lớp đó sẽ bị 'mồ côi' (khóa ngoài tham chiếu vào hư không). Ràng buộc toàn vẹn tham chiếu chặn đứng điều này (trừ khi có thiết lập ON DELETE CASCADE).",
                "explanation": "Toàn vẹn tham chiếu đảm bảo một khóa ngoài phải luôn trỏ tới một bản ghi hợp lệ đang tồn tại ở bảng cha. Không thể xóa hàng cha khi vẫn còn hàng con phụ thuộc."
            },
            {
                "id": 16,
                "question": "Trong câu lệnh SQL, thứ tự thực hiện thực tế của hệ quản trị CSDL khác với thứ tự viết mã. Giai đoạn nào sau đây được thực thi ĐẦU TIÊN?",
                "options": [
                    "A. SELECT",
                    "B. FROM",
                    "C. WHERE",
                    "D. ORDER BY"
                ],
                "answer": 1,
                "trap": "Mặc dù khi viết code chữ `SELECT` luôn đứng đầu dòng, nhưng máy tính phải tìm xem dữ liệu lấy từ BẢNG NÀO (`FROM`) trước, sau đó mới lọc dòng (`WHERE`), rồi mới chọn cột hiển thị (`SELECT`).",
                "explanation": "Thứ tự xử lý logic của SQL: 1. FROM -> 2. WHERE -> 3. GROUP BY -> 4. HAVING -> 5. SELECT -> 6. ORDER BY. Vì vậy ta không thể dùng bí danh (Alias) tạo trong SELECT để làm điều kiện lọc trong WHERE."
            },
            {
                "id": 17,
                "question": "Hàm tổng hợp nào sau đây tính giá trị trung bình của một cột dạng số và tự động bỏ qua các giá trị NULL?",
                "options": [
                    "A. MEDIAN()",
                    "B. AVERAGE()",
                    "C. AVG()",
                    "D. MEAN()"
                ],
                "answer": 2,
                "trap": "Trong Excel người ta dùng hàm `AVERAGE()`, nhưng trong SQL từ khóa chuẩn bắt buộc là `AVG()`. Học sinh nhầm lẫn giữa Excel và SQL rất nhiều.",
                "explanation": "Trong SQL, hàm `AVG(tên_cột)` tính giá trị trung bình cộng của các ô có giá trị trong cột, tự động bỏ qua các hàng chứa giá trị NULL."
            },
            {
                "id": 18,
                "question": "Để cập nhật tăng thêm 1 điểm cho tất cả học sinh thuộc lớp '12A2' trong bảng `DIEM_THI`, câu lệnh SQL nào sau đây là ĐÚNG?",
                "options": [
                    "A. MODIFY DIEM_THI SET Diem = Diem + 1 WHERE MaLop = '12A2';",
                    "B. UPDATE DIEM_THI SET Diem = Diem + 1 WHERE MaLop = '12A2';",
                    "C. CHANGE DIEM_THI ADD 1 TO Diem WHERE MaLop = '12A2';",
                    "D. ALTER TABLE DIEM_THI SET Diem = Diem + 1 WHERE MaLop = '12A2';"
                ],
                "answer": 1,
                "trap": "Lệnh `ALTER TABLE` dùng để sửa CẤU TRÚC bảng (thêm/xóa cột), không dùng để sửa DỮ LIỆU. Muốn sửa dữ liệu dòng phải dùng `UPDATE ... SET ... WHERE ...`.",
                "explanation": "Cú pháp sửa đổi dữ liệu đã có trong bảng là `UPDATE <tên_bảng> SET <cột> = <giá_trị_mới> WHERE <điều_kiện>;`."
            },
            {
                "id": 19,
                "question": "Thuộc tính `AUTO_INCREMENT` (hoặc `IDENTITY`) trong SQL thường được gán cho cột nào?",
                "options": [
                    "A. Cột ghi chú văn bản dài.",
                    "B. Cột số nguyên làm khóa chính, giúp giá trị tự động tăng thêm 1 mỗi khi có một bản ghi mới được chèn vào.",
                    "C. Cột ngày tháng sinh nhật của học sinh.",
                    "D. Cột điểm trung bình môn học."
                ],
                "answer": 1,
                "trap": "Học sinh chọn nhầm sang điểm trung bình hoặc ngày sinh. AUTO_INCREMENT là cơ chế sinh mã tự động (ID: 1, 2, 3...) cho khóa chính.",
                "explanation": "Thuộc tính `AUTO_INCREMENT` tự động sinh giá trị số nguyên tăng dần duy nhất cho mỗi hàng mới chèn vào, rất tiện lợi khi tạo khóa chính nhân tạo (Surrogate Key)."
            },
            {
                "id": 20,
                "question": "Phát biểu nào sau đây thể hiện ưu điểm vượt trội của Hệ quản trị CSDL quan hệ (RDBMS) so với việc lưu trữ dữ liệu bằng các file văn bản (như Word hay Excel) riêng lẻ?",
                "options": [
                    "A. RDBMS không chiếm bất kỳ dung lượng bộ nhớ nào trên ổ cứng máy tính.",
                    "B. RDBMS đảm bảo tính toàn vẹn dữ liệu, giảm thiểu dư thừa, hỗ trợ nhiều người dùng truy cập đồng thời và tính bảo mật cao.",
                    "C. RDBMS là phần mềm miễn phí và không bao giờ xảy ra lỗi.",
                    "D. Người dùng không cần học bất kỳ câu lệnh nào vẫn quản trị được RDBMS."
                ],
                "answer": 1,
                "trap": "Các phương án A, C, D là tuyệt đối hóa phi lý. Ưu thế thực sự của CSDL quan hệ nằm ở tính nhất quán, giảm dư thừa và kiểm soát đa truy cập đồng thời (ACID).",
                "explanation": "RDBMS quản lý dữ liệu có tổ chức, loại bỏ trùng lặp bất hợp lý, kiểm soát quyền truy cập chặt chẽ và đảm bảo tính nhất quán dữ liệu thông qua các ràng buộc khóa và giao dịch (Transaction)."
            }
        ]
    },

    # =========================================================================
    # CHUYÊN ĐỀ 4: HTML VÀ CSS CĂN BẢN (20 CÂU)
    # =========================================================================
    "4": {
        "topic_id": "4",
        "topic_title": "Chuyên đề 4: HTML và CSS căn bản",
        "description": "20 câu trắc nghiệm thiết kế web: Thẻ tự đóng, thẻ khối block vs nội dòng inline, mô hình hộp Box Model, độ ưu tiên CSS Specificity, thuộc tính Position và Semantic HTML.",
        "questions": [
            {
                "id": 1,
                "question": "Thẻ HTML nào sau đây thuộc nhóm thẻ tự đóng (Void/Self-closing Element), nghĩa là KHÔNG CÓ thẻ đóng dạng `</...>`?",
                "options": [
                    "A. `<p>`",
                    "B. `<img>`",
                    "C. `<div>`",
                    "D. `<h1>`"
                ],
                "answer": 1,
                "trap": "⚠️ BẪY THƯỜNG GẶP: Học sinh hay viết nhầm `<img>...</img>`. Thẻ `<img>`, `<br>`, `<hr>`, `<input>`, `<meta>` là các thẻ rỗng (void elements), không có nội dung văn bản kẹp giữa nên không có thẻ đóng.",
                "explanation": "Trong HTML, thẻ `<img>` dùng để nhúng hình ảnh qua thuộc tính `src`, là thẻ tự đóng và không có thẻ đóng `</img>` đi kèm."
            },
            {
                "id": 2,
                "question": "Sự khác biệt cốt lõi giữa phần tử dạng khối (Block-level element) và phần tử nội dòng (Inline element) là gì?",
                "options": [
                    "A. Phần tử Block luôn bắt đầu trên một dòng mới và chiếm toàn bộ chiều rộng có sẵn; còn phần tử Inline chỉ chiếm chiều rộng vừa đủ nội dung và không tự ngắt dòng.",
                    "B. Phần tử Inline có thể đặt được kích thước width và height tùy ý, còn Block thì không.",
                    "C. Phần tử Block chỉ dùng để hiển thị hình ảnh, còn Inline chỉ dùng để hiển thị chữ.",
                    "D. Trình duyệt chỉ hỗ trợ tối đa 5 phần tử Block trên một trang web."
                ],
                "answer": 0,
                "trap": "Học sinh hay nhầm ngược: nghĩ rằng inline đặt được width/height. Phần tử Inline thuần túy (như span, a, b) KHÔNG THỂ áp dụng thuộc tính width và height (trừ khi chuyển sang inline-block hoặc block).",
                "explanation": "Phần tử Block (như div, p, h1) luôn chiếm trọn 100% bề ngang và đẩy phần tử tiếp theo xuống dòng mới. Phần tử Inline (như a, span, strong) nằm trên cùng dòng với văn bản xung quanh."
            },
            {
                "id": 3,
                "question": "Cho một đoạn mã HTML có một phần tử vừa có style nội tuyến, vừa có ID, vừa có Class. Khi có sự xung đột thuộc tính màu chữ (`color`), màu sắc nào sẽ được ưu tiên áp dụng?",
                "options": [
                    "A. Thuộc tính trong bộ chọn ID (#id)",
                    "B. Thuộc tính trong bộ chọn Class (.class)",
                    "C. Thuộc tính viết trực tiếp trong thẻ bằng style nội tuyến (`style=\"color: ...\"`)",
                    "D. Thuộc tính của thẻ tên phần tử (như `p { color: ... }`)"
                ],
                "answer": 2,
                "trap": "⚠️ BẪY THỨ TỰ ƯU TIÊN CSS (Specificity): Độ ưu tiên theo thang: Style nội tuyến (Inline style = 1000) > ID selector (100) > Class selector (10) > Element selector (1). Trừ khi có `!important`, style nội tuyến luôn đánh bại ID.",
                "explanation": "Quy tắc Specificity trong CSS quy định: Style trực tiếp trong thuộc tính `style=\"...\"` của thẻ HTML có độ ưu tiên cao hơn mọi khai báo CSS trong thẻ `<style>` hoặc file CSS bên ngoài (nếu không có cờ `!important`)."
            },
            {
                "id": 4,
                "question": "Mô hình hộp (Box Model) trong CSS bao gồm 4 thành phần tính từ TRONG RA NGOÀI theo đúng thứ tự nào sau đây?",
                "options": [
                    "A. Margin -> Border -> Padding -> Content",
                    "B. Content -> Padding -> Border -> Margin",
                    "C. Content -> Margin -> Border -> Padding",
                    "D. Padding -> Content -> Border -> Margin"
                ],
                "answer": 1,
                "trap": "Học sinh rất hay nhầm lẫn giữa Padding (khoảng đệm giữa nội dung và viền) và Margin (khoảng lề ngoài viền để cách xa các phần tử khác).",
                "explanation": "Box Model chuẩn tính từ tâm ra ngoài gồm: 1. Content (Nội dung) -> 2. Padding (Khoảng đệm) -> 3. Border (Đường viền) -> 4. Margin (Lề ngoài)."
            },
            {
                "id": 5,
                "question": "Thuộc tính CSS `position: absolute;` sẽ định vị phần tử dựa theo mốc nào sau đây?",
                "options": [
                    "A. Luôn luôn căn theo góc trên cùng bên trái của màn hình trình duyệt (viewport).",
                    "B. Căn theo vị trí ban đầu của chính phần tử đó trước khi dịch chuyển.",
                    "C. Căn tương đối theo phần tử tổ tiên (cha, ông) gần nhất có thuộc tính `position` mang giá trị khác `static` (như relative, absolute, fixed).",
                    "D. Căn tự động vào vị trí chính giữa màn hình."
                ],
                "answer": 2,
                "trap": "Nhiều bạn nghĩ `absolute` luôn bám theo cửa sổ màn hình (đó là `position: fixed`). `absolute` chỉ bám theo cửa sổ nếu TẤT CẢ các thẻ cha chứa nó đều là `static`.",
                "explanation": "`position: absolute` sẽ tìm phần tử tổ tiên gần nhất có position tương đối (thường là `position: relative`) làm hệ quy chiếu tọa độ top, left, right, bottom."
            },
            {
                "id": 6,
                "question": "Thẻ Semantic nào trong HTML5 được sử dụng để định nghĩa khu vực chứa các liên kết điều hướng (menu) của trang web?",
                "options": [
                    "A. `<menu-bar>`",
                    "B. `<nav>`",
                    "C. `<navigation>`",
                    "D. `<links>`"
                ],
                "answer": 1,
                "trap": "HTML5 không có thẻ `<navigation>` hay `<menu-bar>`. Thẻ chuẩn ngữ nghĩa quy định trong W3C là thẻ `<nav>` (viết tắt của navigation).",
                "explanation": "Thẻ `<nav>` (Navigation) là thẻ ngữ nghĩa HTML5 chỉ định khu vực dành riêng cho các liên kết điều hướng chính trong website, giúp các công cụ tìm kiếm và trình đọc màn hình hiểu cấu trúc trang."
            },
            {
                "id": 7,
                "question": "Thuộc tính `alt` trong thẻ `<img>` có vai trò quan trọng nhất là gì?",
                "options": [
                    "A. Đặt kích thước chiều rộng tự động cho hình ảnh.",
                    "B. Cung cấp văn bản thay thế mô tả nội dung hình ảnh khi ảnh bị lỗi không tải được hoặc hỗ trợ phần mềm đọc màn hình cho người khiếm thị.",
                    "C. Tạo hiệu ứng viền phát sáng khi người dùng di chuột qua bức ảnh.",
                    "D. Tự động chuyển đổi định dạng ảnh từ PNG sang JPG."
                ],
                "answer": 1,
                "trap": "Nhiều bạn nghĩ `alt` là chú thích ảnh hiển thị ở dưới (đó là `<figcaption>`). Thuộc tính `alt` (Alternative Text) là văn bản thay thế khi ảnh hỏng và phục vụ tính tiếp cận (Accessibility).",
                "explanation": "Thuộc tính `alt` mang tính bắt buộc theo chuẩn web để mô tả nội dung ảnh cho người khiếm thị dùng Screen Reader và hiển thị khi đường dẫn ảnh bị gãy."
            },
            {
                "id": 8,
                "question": "Trong CSS, bộ chọn (Selector) nào sau đây chọn TẤT CẢ các thẻ `<p>` nằm TRỰC TIẾP bên trong thẻ `<div class=\"container\">` (con trực tiếp cấp 1)?",
                "options": [
                    "A. `.container p`",
                    "B. `.container > p`",
                    "C. `.container + p`",
                    "D. `.container ~ p`"
                ],
                "answer": 1,
                "trap": "Dấu cách (`.container p`) chọn TẤT CẢ con cháu (kể cả cháu, chắt nằm sâu bên trong). Chỉ có dấu `>` mới là Child Combinator (chọn đúng con trực tiếp cấp 1).",
                "explanation": "Toán tử `>` trong CSS là Child Selector, chỉ nhắm mục tiêu vào các phần tử con trực tiếp cấp 1 của phần tử cha được chỉ định."
            },
            {
                "id": 9,
                "question": "Để mở một liên kết sang một tab mới (cửa sổ mới) của trình duyệt khi người dùng bấm vào thẻ `<a>`, ta sử dụng thuộc tính nào?",
                "options": [
                    "A. `new=\"tab\"`",
                    "B. `target=\"_blank\"`",
                    "C. `window=\"new\"`",
                    "D. `href=\"_new\"`"
                ],
                "answer": 1,
                "trap": "Học sinh hay nhớ nhầm thành `target=\"_new\"` hoặc gõ thiếu dấu gạch dưới `_`. Chuẩn HTML bắt buộc là `target=\"_blank\"`.",
                "explanation": "Thuộc tính `target=\"_blank\"` trong thẻ siêu liên kết `<a>` hướng dẫn trình duyệt mở tài liệu được liên kết trong một tab hoặc cửa sổ mới hoàn toàn."
            },
            {
                "id": 10,
                "question": "Thuộc tính CSS `box-sizing: border-box;` đem lại lợi ích thiết thực nào trong quá trình bố cục giao diện?",
                "options": [
                    "A. Tự động vẽ một đường viền nét đứt màu đỏ quanh tất cả các phần tử.",
                    "B. Giữ cho tổng chiều rộng của phần tử không bị phình to ra khi ta thêm padding và border, vì padding và border sẽ được tính gộp vào bên trong width.",
                    "C. Xóa bỏ hoàn toàn khoảng lề margin giữa các phần tử.",
                    "D. Tự động chuyển đổi trang web thành giao diện 3D."
                ],
                "answer": 1,
                "trap": "Mặc định (`content-box`), nếu đặt width: 100px mà thêm padding: 10px thì tổng bề ngang thành 120px làm vỡ khung giao diện. Thuộc tính `border-box` giải quyết triệt để lỗi này.",
                "explanation": "Với `box-sizing: border-box;`, kích thước `width` và `height` của phần tử bao gồm cả phần content, padding và border, giúp lập trình viên tính toán kích thước layout chuẩn xác và không bị tràn khung."
            },
            {
                "id": 11,
                "question": "Để nhóm các ô dữ liệu trên cùng một dòng trong bảng HTML (`<table>`), ta sử dụng thẻ nào?",
                "options": [
                    "A. `<td>`",
                    "B. `<tr>`",
                    "C. `<th>`",
                    "D. `<tc>`"
                ],
                "answer": 1,
                "trap": "Học sinh hay nhầm giữa `<tr>` (Table Row - dòng) và `<td>` (Table Data - ô dữ liệu). Một dòng `<tr>` chứa nhiều ô `<td>`.",
                "explanation": "Thẻ `<tr>` (Table Row) định nghĩa một hàng ngang trong bảng; bên trong `<tr>` chứa các thẻ tiêu đề cột `<th>` hoặc ô dữ liệu `<td>`."
            },
            {
                "id": 12,
                "question": "Cặp thẻ nào sau đây dùng để nhúng mã JavaScript trực tiếp vào trang web HTML?",
                "options": [
                    "A. `<javascript> ... </javascript>`",
                    "B. `<script> ... </script>`",
                    "C. `<code> ... </code>`",
                    "D. `<js> ... </js>`"
                ],
                "answer": 1,
                "trap": "Nhiều bạn tưởng thẻ tên là `<javascript>`. Thẻ HTML chuẩn của W3C từ trước tới nay là thẻ `<script>`.",
                "explanation": "Thẻ `<script>` dùng để nhúng mã lệnh thực thi phía máy khách (thường là JavaScript) hoặc liên kết đến file script bên ngoài qua thuộc tính `src`."
            },
            {
                "id": 13,
                "question": "Trong biểu mẫu HTML (`<form>`), phương thức `method=\"POST\"` khác với `method=\"GET\"` ở điểm căn bản nào?",
                "options": [
                    "A. POST gửi dữ liệu ngầm trong phần thân (Body) của yêu cầu HTTP và không hiển thị dữ liệu trên thanh địa chỉ URL, phù hợp gửi mật khẩu.",
                    "B. GET truyền dữ liệu an toàn hơn POST rất nhiều lần.",
                    "C. POST chỉ gửi được tối đa 255 ký tự chữ cái, không gửi được số.",
                    "D. GET bắt buộc người dùng phải có tài khoản quản trị mới gửi được form."
                ],
                "answer": 0,
                "trap": "Học sinh nhầm tưởng GET và POST chỉ khác nhau ở chữ cái. GET đính kèm toàn bộ dữ liệu lên thanh URL (ai nhìn vào màn hình cũng thấy mật khẩu). POST bảo mật hơn và gửi được khối lượng dữ liệu lớn.",
                "explanation": "Phương thức GET nối dữ liệu vào chuỗi truy vấn (query string) trên URL. Phương thức POST đóng gói dữ liệu trong Message Body, bảo vệ thông tin riêng tư và truyền được file dung lượng lớn."
            },
            {
                "id": 14,
                "question": "Thuộc tính CSS nào sau đây được sử dụng để làm cho văn bản hiển thị in đậm?",
                "options": [
                    "A. `font-style: bold;`",
                    "B. `text-decoration: bold;`",
                    "C. `font-weight: bold;`",
                    "D. `font-variant: bold;`"
                ],
                "answer": 2,
                "trap": "Học sinh hay nhầm với `font-style` (font-style dùng cho in nghiêng: italic). Độ đậm nhạt của chữ bắt buộc dùng `font-weight` (bold hoặc 700).",
                "explanation": "Thuộc tính `font-weight` xác định độ dày nét chữ (đậm/nhạt), có thể nhận các giá trị như normal, bold, bolder, hoặc số từ 100 đến 900."
            },
            {
                "id": 15,
                "question": "Trong mô hình Flexbox của CSS, để căn chỉnh các phần tử con nằm theo chiều ngang vào chính giữa khung chứa (trục chính Main Axis), ta sử dụng thuộc tính:",
                "options": [
                    "A. `align-items: center;`",
                    "B. `justify-content: center;`",
                    "C. `text-align: center;`",
                    "D. `vertical-align: middle;`"
                ],
                "answer": 1,
                "trap": "Cặp đôi nhầm lẫn kinh điển trong Flexbox: `justify-content` căn theo trục chính (Main Axis - mặc định là chiều ngang), còn `align-items` căn theo trục phụ (Cross Axis - chiều dọc).",
                "explanation": "Khi `flex-direction: row` (mặc định), `justify-content: center;` phân phối và căn chỉnh các phần tử con vào chính giữa trục chính (ngang)."
            },
            {
                "id": 16,
                "question": "Thẻ danh sách nào sau đây hiển thị các mục con theo thứ tự đánh số (1, 2, 3...)?",
                "options": [
                    "A. `<ul>` (Unordered List)",
                    "B. `<ol>` (Ordered List)",
                    "C. `<dl>` (Description List)",
                    "D. `<li>` (List Item)"
                ],
                "answer": 1,
                "trap": "`<ul>` là danh sách không thứ tự (dấu chấm bullet tròn). `<ol>` là Ordered List (danh sách có thứ tự được đánh số)."
            },
            {
                "id": 17,
                "question": "Khai báo mã màu nào sau đây trong CSS biểu diễn màu TRẮNG tinh khiết?",
                "options": [
                    "A. `#000000`",
                    "B. `#ffffff`",
                    "C. `rgb(0, 0, 0)`",
                    "D. `#ff0000`"
                ],
                "answer": 1,
                "trap": "`#000000` hoặc `rgb(0, 0, 0)` là màu ĐEN (không có ánh sáng). Màu TRẮNG (tất cả các kênh ánh sáng Đỏ, Xanh lá, Xanh dương đều đạt mức tối đa 255) là `#ffffff` hoặc `rgb(255, 255, 255)`.",
                "explanation": "Trong hệ màu cộng RGB, màu trắng tạo thành từ việc kết hợp cường độ cao nhất của 3 màu cơ bản: Red=FF, Green=FF, Blue=FF -> `#ffffff`."
            },
            {
                "id": 18,
                "question": "Thẻ `<input type=\"radio\">` khác với thẻ `<input type=\"checkbox\">` ở điểm quan trọng nào?",
                "options": [
                    "A. Checkbox cho phép người dùng tích chọn nhiều phương án cùng lúc; còn các Radio button có cùng thuộc tính `name` chỉ cho phép chọn DUY NHẤT 1 phương án.",
                    "B. Radio chỉ hiển thị được trên màn hình cảm ứng, máy tính không bấm được.",
                    "C. Checkbox chỉ chứa được số, Radio chỉ chứa được chữ.",
                    "D. Không có điểm khác nhau nào, chỉ là cách đổi giao diện vuông thành tròn."
                ],
                "answer": 0,
                "trap": "Học sinh hay quên gán thuộc tính `name` giống nhau cho các radio button, dẫn đến việc chọn được nhiều radio cùng lúc. Nếu có cùng `name`, radio chỉ cho phép chọn 1 duy nhất (như chọn Giới tính Nam/Nữ).",
                "explanation": "Radio button dùng cho các lựa chọn loại trừ lẫn nhau (chỉ chọn 1 trong nhóm có chung `name`). Checkbox dùng cho các lựa chọn độc lập (có thể chọn 0, 1 hoặc nhiều)."
            },
            {
                "id": 19,
                "question": "Để liên kết một file CSS bên ngoài có tên `style.css` vào trang HTML, ta đặt thẻ nào vào bên trong phần `<head>`?",
                "options": [
                    "A. `<style src=\"style.css\"></style>`",
                    "B. `<link rel=\"stylesheet\" href=\"style.css\">`",
                    "C. `<include css=\"style.css\">`",
                    "D. `<script href=\"style.css\"></script>`"
                ],
                "answer": 1,
                "trap": "Nhiều bạn dùng thẻ `<style src=...>`, thẻ `<style>` không có thuộc tính src! Để nối file css bên ngoài bắt buộc dùng thẻ `<link rel=\"stylesheet\" href=\"...\">`.",
                "explanation": "Cú pháp chuẩn HTML để nạp tệp định kiểu bên ngoài là dùng thẻ đơn `<link>` với thuộc tính `rel=\"stylesheet\"` và đường dẫn file trong `href`."
            },
            {
                "id": 20,
                "question": "Thuộc tính `display: none;` khác với `visibility: hidden;` trong CSS ở điểm cốt lõi nào?",
                "options": [
                    "A. `display: none;` ẩn phần tử và XÓA BỎ HOÀN TOÀN khoảng không gian chiếm chỗ của nó trên trang; còn `visibility: hidden;` chỉ làm vô hình nhưng VẪN GIỮ NGUYÊN KHOẢNG TRỐNG chiếm chỗ đó.",
                    "B. `visibility: hidden;` sẽ xóa luôn phần tử khỏi cây DOM của HTML.",
                    "C. Hai thuộc tính này giống hệt nhau, không có sự khác biệt nào.",
                    "D. `display: none;` chỉ dùng được trên điện thoại di động."
                ],
                "answer": 0,
                "trap": "⚠️ BẪY GIAO DIỆN KINH ĐIỂN: `display: none` làm phần tử biến mất như chưa từng tồn tại, các phần tử xung quanh lấp vào chỗ trống. Còn `visibility: hidden` để lại một khoảng trống to tướng trống trơn trên trang web.",
                "explanation": "`display: none` loại phần tử ra khỏi luồng bố cục layout của trang. `visibility: hidden` chỉ ẩn hiển thị trực quan nhưng phần tử vẫn chiếm trọn diện tích hộp trong không gian trang."
            }
        ]
    },

    # =========================================================================
    # CHUYÊN ĐỀ 5: BẢO MẬT, AN TOÀN HỆ THỐNG VÀ KHẮC PHỤC SỰ CỐ (20 CÂU)
    # =========================================================================
    "5": {
        "topic_id": "5",
        "topic_title": "Chuyên đề 5: Bảo mật, An toàn và Khắc phục sự cố",
        "description": "20 câu trắc nghiệm an ninh mạng: Mã hóa đối xứng & bất đối xứng, chữ ký số, phân loại mã độc Virus/Worm/Trojan/Ransomware, tấn công Phishing, DDoS, tường lửa và xác thực đa yếu tố MFA.",
        "questions": [
            {
                "id": 1,
                "question": "Trong hệ thống mã hóa bất đối xứng (khóa công khai RSA), nếu bạn A muốn gửi một bức thư mật cho bạn B mà chỉ duy nhất bạn B đọc được, bạn A phải dùng chìa khóa nào để mã hóa bức thư?",
                "options": [
                    "A. Khóa bí mật (Private Key) của bạn A",
                    "B. Khóa công khai (Public Key) của bạn A",
                    "C. Khóa công khai (Public Key) của bạn B",
                    "D. Khóa bí mật (Private Key) của bạn B"
                ],
                "answer": 2,
                "trap": "⚠️ BẪY ĐỀ THI SỐ 1 VỀ MÃ HÓA: Học sinh hay chọn A (khóa bí mật của A) hoặc D (khóa bí mật của B). Hãy nhớ nguyên tắc: Muốn gửi đồ vào hòm thư cho B thì phải dùng KHÓA CÔNG KHAI CỦA B để khóa nắp hộp lại. Khi hộp tới nơi, chỉ có B (người duy nhất giữ Khóa bí mật của B) mới mở được!",
                "explanation": "Trong mã hóa bất đối xứng, người gửi sử dụng Khóa công khai (Public Key) của người nhận để mã hóa dữ liệu. Chỉ có Khóa bí mật (Private Key) tương ứng của người nhận mới có thể giải mã được."
            },
            {
                "id": 2,
                "question": "Ngược lại với mã hóa dữ liệu, trong cơ chế Chữ ký số điện tử (Digital Signature), người gửi A sẽ dùng chìa khóa nào để KÝ vào văn bản nhằm chứng minh văn bản do chính mình tạo ra?",
                "options": [
                    "A. Khóa bí mật (Private Key) của người gửi A",
                    "B. Khóa công khai (Public Key) của người gửi A",
                    "C. Khóa công khai (Public Key) của người nhận B",
                    "D. Khóa bí mật (Private Key) của người nhận B"
                ],
                "answer": 0,
                "trap": "Học sinh rất dễ lẫn lộn giữa chiều gửi thư mật và chiều ký số. Ký số thì PHẢI DÙNG KHÓA BÍ MẬT CỦA MÌNH để ký, sau đó người khác dùng Khóa công khai của mình để kiểm tra xác thực chữ ký.",
                "explanation": "Chữ ký số sử dụng Khóa bí mật của người gửi để mã hóa bản băm (hash) của văn bản. Người nhận dùng Khóa công khai của người gửi để giải mã và so khớp, đảm bảo tính toàn vẹn và chống chối bỏ."
            },
            {
                "id": 3,
                "question": "Loại mã độc (Malware) nào sau đây có khả năng TỰ NHÂN BẢN và TỰ ĐỘNG LAN TRUYỀN qua mạng Internet sang các máy tính khác mà KHÔNG CẦN sự can thiệp của con người hay phải gắn vào một file chủ?",
                "options": [
                    "A. Virus máy tính",
                    "B. Sâu máy tính (Worm)",
                    "C. Trojan Horse",
                    "D. Spyware"
                ],
                "answer": 1,
                "trap": "⚠️ BẪY PHÂN BIỆT VIRUS VÀ WORM: Virus bắt buộc phải có file vật chủ (như file .exe, word) và cần con người bấm chạy file đó thì mới lây lan. Còn Worm (Sâu máy tính) hoàn toàn độc lập, tự quét mạng và tự bò sang máy tính khác qua lỗ hổng bảo mật.",
                "explanation": "Sâu máy tính (Worm) là chương trình mã độc độc lập, có khả năng tự sao chép và tự lây lan qua kết nối mạng máy tính mà không cần bất kỳ tương tác nào từ phía người dùng."
            },
            {
                "id": 4,
                "question": "Một người bạn gửi cho em một file có tên 'Game_Hay_Full_Crack.exe'. Khi bấm mở file, em thấy một trò chơi nhỏ hiện lên nhưng thực chất bên dưới máy tính đã bị kẻ xấu bí mật cài một cổng hậu (Backdoor) chiếm quyền điều khiển. Đây là hình thức tấn công bằng loại mã độc nào?",
                "options": [
                    "A. Ransomware",
                    "B. Trojan Horse (Ngựa thành Troy)",
                    "C. Sâu máy tính (Worm)",
                    "D. Adware"
                ],
                "answer": 1,
                "trap": "Đặc trưng của Trojan Horse là 'đội lốt một phần mềm hữu ích, hấp dẫn' để đánh lừa nạn nhân tự tay cài đặt vào máy.",
                "explanation": "Trojan Horse (Ngựa thành Troy) là phần mềm ngụy trang dưới dạng một ứng dụng hợp pháp, vô hại nhằm lừa người dùng cài đặt, sau đó kích hoạt các hành vi độc hại ẩn giấu bên trong."
            },
            {
                "id": 5,
                "question": "Loại mã độc nào sau đây tự động mã hóa toàn bộ tài liệu, ảnh, video của nạn nhân bằng thuật toán cực mạnh và yêu cầu nạn nhân phải trả tiền chuộc (thường bằng tiền mã hóa) để lấy chìa khóa giải mã?",
                "options": [
                    "A. Keylogger",
                    "B. Ransomware (Mã độc tống tiền)",
                    "C. Spyware (Phần mềm gián điệp)",
                    "D. Rootkit"
                ],
                "answer": 1,
                "trap": "Từ khóa quyết định: 'Mã hóa dữ liệu và tống tiền' -> Ransomware (Ransom = Tiền chuộc).",
                "explanation": "Ransomware (mã độc tống tiền) khóa quyền truy cập vào hệ thống hoặc mã hóa toàn bộ dữ liệu quan trọng trên máy nạn nhân, buộc họ phải trả tiền chuộc để nhận khóa giải mã."
            },
            {
                "id": 6,
                "question": "Hình thức tấn công mạng 'Phishing' (Tấn công giả mạo) hoạt động chủ yếu dựa trên kỹ thuật nào?",
                "options": [
                    "A. Sử dụng máy tính siêu mạnh để bẻ khóa mật khẩu trong 1 giây.",
                    "B. Tạo ra các email, tin nhắn hoặc website giả mạo hệt như các ngân hàng, mạng xã hội uy tín để lừa người dùng tự nguyện nhập mật khẩu và mã OTP vào.",
                    "C. Cắt đứt các tuyến cáp quang ngầm dưới biển.",
                    "D. Phát sóng từ trường mạnh để làm hỏng ổ cứng máy tính."
                ],
                "answer": 1,
                "trap": "Phishing (đọc giống Fishing - câu cá) là hình thức lừa đảo thao túng tâm lý (Social Engineering), dụ dỗ con mồi tự cắn câu chứ không phải tấn công bẻ khóa thuật toán bằng máy tính lượng tử.",
                "explanation": "Phishing là phương thức lừa đảo giả danh các tổ chức uy tín (ngân hàng, Facebook, Google) qua email, tin nhắn để dụ nạn nhân cung cấp thông tin bí mật như mật khẩu, số thẻ tín dụng."
            },
            {
                "id": 7,
                "question": "Xác thực hai yếu tố (2FA / Multi-Factor Authentication) yêu cầu kết hợp ít nhất 2 trong 3 nhóm yếu tố nào sau đây?",
                "options": [
                    "A. Mật khẩu cấp 1 và Mật khẩu cấp 2 (đều là điều bạn biết).",
                    "B. Điều bạn biết (Mật khẩu/PIN) + Điều bạn có (Điện thoại/Mã OTP/Thẻ thông minh) + Điều thuộc về bạn (Sinh trắc học: Vân tay/Khuôn mặt).",
                    "C. Tên đăng nhập viết hoa và Tên đăng nhập viết thường.",
                    "D. Câu hỏi bí mật số 1 và Câu hỏi bí mật số 2."
                ],
                "answer": 1,
                "trap": "⚠️ BẪY THƯỜNG GẶP: Hai mật khẩu khác nhau KHÔNG PHẢI là 2FA vì cả hai đều thuộc nhóm 'Điều bạn biết' (Something you know). 2FA bắt buộc phải kết hợp 2 nhóm KHÁC NHAU (ví dụ: Mật khẩu + Mã gửi về điện thoại).",
                "explanation": "3 yếu tố xác thực chuẩn quốc tế gồm: 1. Knowledge (Điều bạn biết: pass, pin); 2. Possession (Điều bạn có: điện thoại, token USB); 3. Inherence (Đặc điểm sinh trắc: vân tay, mống mắt, FaceID)."
            },
            {
                "id": 8,
                "question": "Phát biểu nào sau đây là ĐÚNG khi nói về giới hạn khả năng của Tường lửa (Firewall)?",
                "options": [
                    "A. Tường lửa ngăn chặn được 100% mọi loại virus và mã độc xâm nhập vào máy tính.",
                    "B. Tường lửa chỉ kiểm soát và lọc các luồng dữ liệu mạng ra/vào dựa trên quy tắc bảo mật; không thể ngăn chặn virus nếu người dùng chủ động tải về và chạy file đính kèm từ email.",
                    "C. Khi đã bật tường lửa thì máy tính không bao giờ cần cài mật khẩu nữa.",
                    "D. Tường lửa chỉ có dạng phần cứng, không thể cài đặt dưới dạng phần mềm."
                ],
                "answer": 1,
                "trap": "Nhiều học sinh thần thánh hóa Tường lửa: tưởng có firewall là bất tử. Firewall là người gác cổng kiểm tra cổng (port) và địa chỉ IP, nếu bạn tự tay mang virus qua cổng thì firewall không thể cứu bạn.",
                "explanation": "Tường lửa (Firewall) giám sát và lọc lưu lượng mạng theo các quy tắc thiết lập trước. Nó không thể phát hiện các cuộc tấn công lừa đảo tâm lý hoặc mã độc đã được đóng gói an toàn trong các luồng dữ liệu hợp lệ mà người dùng cho phép tải về."
            },
            {
                "id": 9,
                "question": "Tấn công từ chối dịch vụ phân tán (DDoS - Distributed Denial of Service) làm tê liệt máy chủ nạn nhân bằng cách nào?",
                "options": [
                    "A. Tự động xóa sạch mã nguồn của máy chủ trong vòng 1 giây.",
                    "B. Sử dụng mạng lưới hàng nghìn máy tính ma (Botnet) đồng loạt gửi một lượng khổng lồ yêu cầu giả mạo tới máy chủ, làm máy chủ cạn kiệt băng thông và tài nguyên xử lý dẫn đến sập mạng.",
                    "C. Thay đổi mật khẩu tài khoản quản trị của máy chủ.",
                    "D. Làm đứt nguồn điện cung cấp cho phòng máy chủ."
                ],
                "answer": 1,
                "trap": "DDoS không hề đánh cắp hay xóa dữ liệu. Mục đích duy nhất của DDoS là làm máy chủ 'nghẹt thở' vì quá tải yêu cầu giả, khiến người dùng thật không thể truy cập được dịch vụ.",
                "explanation": "Tấn công DDoS huy động mạng máy tính ma (Botnet) gửi hàng triệu yêu cầu truy cập cùng lúc, làm tràn ngập băng thông và quá tải CPU/RAM của mục tiêu khiến dịch vụ bị gián đoạn."
            },
            {
                "id": 10,
                "question": "Để tạo một mật khẩu mạnh và an toàn, khuyến nghị nào sau đây là CHUẨN XÁC NHẤT?",
                "options": [
                    "A. Dùng ngày tháng năm sinh hoặc số điện thoại của mình để không bao giờ bị quên.",
                    "B. Dùng từ 'password123' vì có cả chữ và số.",
                    "C. Độ dài tối thiểu từ 12 ký tự trở lên, kết hợp chữ hoa, chữ thường, chữ số và các ký tự đặc biệt (như @, #, $, !), không dùng thông tin cá nhân dễ đoán.",
                    "D. Đặt một mật khẩu duy nhất và dùng chung cho tất cả các tài khoản ngân hàng, email, mạng xã hội."
                ],
                "answer": 2,
                "trap": "Dùng thông tin cá nhân (sinh nhật, tên người yêu) là miếng mồi ngon cho kỹ thuật tấn công dò từ điển (Dictionary attack). Dùng chung 1 mật khẩu cho mọi trang là thói quen cực kỳ nguy hiểm.",
                "explanation": "Mật khẩu mạnh phải có độ dài từ 12 ký tự trở lên, không có nghĩa trong từ điển, trộn lẫn chữ hoa, chữ thường, số, ký tự đặc biệt và không tái sử dụng trên nhiều nền tảng khác nhau."
            },
            {
                "id": 11,
                "question": "Phần mềm gián điệp theo dõi thao tác bàn phím có tên gọi là gì?",
                "options": [
                    "A. Ransomware",
                    "B. Keylogger",
                    "C. Adware",
                    "D. Antivirus"
                ],
                "answer": 1,
                "trap": "Key (Phím) + Logger (Ghi nhật ký) = Keylogger. Phần mềm này bí mật ghi lại mọi phím bấm của người dùng để đánh cắp tên đăng nhập và mật khẩu.",
                "explanation": "Keylogger là một dạng Spyware chuyên ghi lại các thao tác nhấn phím trên bàn phím máy tính để thu thập dữ liệu nhạy cảm của người dùng rồi gửi về cho kẻ tấn công."
            },
            {
                "id": 12,
                "question": "Kỹ thuật 'Tấn công phi kỹ thuật' (Social Engineering) nhắm vào điểm yếu cốt lõi nào trong hệ thống an ninh thông tin?",
                "options": [
                    "A. Điểm yếu trong thuật toán mã hóa AES 256-bit.",
                    "B. Yếu tố con người (sự nhẹ dạ cả tin, lòng tham, sự sợ hãi hoặc thiếu hiểu biết của người dùng).",
                    "C. Độ trễ của dây cáp quang xuyên đại dương.",
                    "D. Hệ thống tản nhiệt nước của máy chủ."
                ],
                "answer": 1,
                "trap": "Nhiều người nghĩ hacker chỉ tấn công code phần mềm. Thực tế 'con người là mắt xích yếu nhất trong chuỗi bảo mật'. Kẻ xấu dùng đòn tâm lý để nạn nhân tự dâng nộp mật khẩu.",
                "explanation": "Social Engineering là nghệ thuật thao túng tâm lý con người để họ tự nguyện tiết lộ thông tin bí mật hoặc thực hiện các hành động vi phạm quy tắc an toàn bảo mật."
            },
            {
                "id": 13,
                "question": "Hành vi sử dụng phần mềm bẻ khóa (Crack/Patch) tải từ các trang web trôi nổi trên mạng tiềm ẩn rủi ro bảo mật lớn nhất nào?",
                "options": [
                    "A. Phần mềm crack chạy nhanh gấp đôi phần mềm bản quyền.",
                    "B. Kẻ cung cấp bản crack thường đã bí mật nhúng sẵn mã độc (Trojan, Keylogger, Ransomware) vào bên trong file kích hoạt để kiểm soát máy tính của người tải.",
                    "C. Máy tính sẽ bị tự động nâng cấp RAM miễn phí.",
                    "D. Màn hình máy tính bị đổi sang màu hồng."
                ],
                "answer": 1,
                "trap": "Không có bữa trưa nào miễn phí. Các file kích hoạt bẻ khóa thường yêu cầu người dùng 'Tắt phần mềm diệt virus trước khi chạy', tạo điều kiện cho mã độc thả vào hệ điều hành mà không bị phát hiện.",
                "explanation": "Phần mềm bẻ khóa vi phạm luật sở hữu trí tuệ và là con đường phát tán mã độc nguy hiểm nhất, vì file crack thường chứa sẵn backdoor để biến máy tính nạn nhân thành máy tính ma."
            },
            {
                "id": 14,
                "question": "Mục đích của việc thường xuyên sao lưu dữ liệu (Backup) ra ổ cứng ngoài hoặc dịch vụ lưu trữ đám mây độc lập là gì?",
                "options": [
                    "A. Giúp máy tính khởi động nhanh hơn 50%.",
                    "B. Đảm bảo có thể phục hồi lại dữ liệu quan trọng khi máy tính bị hỏng ổ cứng, bị mất cắp hoặc bị mã độc Ransomware mã hóa dữ liệu tống tiền.",
                    "C. Tự động sửa chữa các lỗi chính tả có trong bài tiểu luận.",
                    "D. Giúp máy tính không bao giờ bị nóng khi chơi game."
                ],
                "answer": 1,
                "trap": "Học sinh hay coi nhẹ việc Backup dữ liệu cho đến khi bị dính Ransomware. Khi bị mã hóa, cách duy nhất để lấy lại dữ liệu mà không cần trả tiền chuộc là phục hồi từ bản Backup sạch.",
                "explanation": "Sao lưu dữ liệu định kỳ theo nguyên tắc 3-2-1 là biện pháp phòng thủ tối thượng giúp bảo vệ thông tin trước mọi sự cố hư hỏng phần cứng, thiên tai hoặc tấn công mã độc."
            },
            {
                "id": 15,
                "question": "Khi sử dụng mạng Wi-Fi công cộng (tại quán cà phê, sân bay, nhà ga) mà không có mật khẩu bảo vệ, rủi ro an ninh mạng nào sau đây có khả năng xảy ra cao nhất?",
                "options": [
                    "A. Kẻ xấu trong cùng mạng có thể sử dụng kỹ thuật nghe lén (Sniffing/Man-in-the-Middle) để bắt các gói tin dữ liệu chưa được mã hóa mà thiết bị gửi/nhận.",
                    "B. Điện thoại của người dùng sẽ tự động bị nổ pin.",
                    "C. Mạng Wi-Fi công cộng sẽ tự động xóa sạch thẻ nhớ điện thoại.",
                    "D. Mọi thông tin trong điện thoại sẽ bị in ra giấy tại quán cà phê."
                ],
                "answer": 0,
                "trap": "Wi-Fi công cộng mở không có mã hóa tầng liên kết. Bất kỳ ai trong cùng mạng dùng phần mềm nghe lén (như Wireshark) đều có thể thu thập các gói tin chưa mã hóa truyền qua không khí.",
                "explanation": "Mạng Wi-Fi công cộng không an toàn dễ bị tấn công nghe lén (Eavesdropping) hoặc tấn công giả mạo điểm truy cập (Evil Twin). Người dùng nên sử dụng VPN khi buộc phải dùng Wi-Fi công cộng."
            },
            {
                "id": 16,
                "question": "Tấn công kiểu 'Đoán vét cạn' (Brute Force Attack) vào mật khẩu hoạt động theo nguyên tắc nào?",
                "options": [
                    "A. Dùng máy tính thử lần lượt từng tổ hợp ký tự có thể có cho đến khi trùng khớp với mật khẩu chính xác.",
                    "B. Gửi email dọa dẫm để nạn nhân tự gửi mật khẩu qua bưu điện.",
                    "C. Cắt đứt dây mạng Internet của máy chủ ngân hàng.",
                    "D. Cài đặt hệ điều hành mới đè lên hệ điều hành cũ."
                ],
                "answer": 0,
                "trap": "Brute Force là tấn công bằng vũ lực tính toán: thử A, B, C... AA, AB... 0000, 0001... Đó là lý do tại sao các hệ thống bảo mật hiện đại luôn khóa tài khoản sau 5 lần nhập sai liên tiếp.",
                "explanation": "Tấn công Brute Force thử tất cả các khả năng kết hợp của ký tự theo cấp số nhân. Mật khẩu càng ngắn và đơn giản thì thời gian bị Brute Force bẻ khóa càng nhanh."
            },
            {
                "id": 17,
                "question": "Bản vá bảo mật (Security Patch) do các hãng phần mềm (như Microsoft, Google, Apple) phát hành định kỳ có vai trò gì?",
                "options": [
                    "A. Làm máy tính chạy chậm lại để ép người dùng mua máy mới.",
                    "B. Sửa chữa các lỗ hổng bảo mật mới được phát hiện trong hệ điều hành hoặc phần mềm, ngăn chặn tin tặc khai thác xâm nhập.",
                    "C. Đổi màu hình nền màn hình máy tính.",
                    "D. Tự động xóa bỏ các file video của người dùng."
                ],
                "answer": 1,
                "trap": "Nhiều người lười cập nhật Windows Update vì sợ lâu, nhưng hầu hết các cuộc tấn công mã độc quy mô toàn cầu (như WannaCry) đều nhắm vào các máy tính chưa chịu cài bản vá lỗi bảo mật.",
                "explanation": "Bản vá bảo mật (Security Patch) khắc phục các lỗ hổng mã nguồn (vulnerability) trước khi tin tặc kịp vũ khí hóa thành các cuộc tấn công Zero-day hoặc khai thác từ xa."
            },
            {
                "id": 18,
                "question": "Mã hóa đối xứng (Symmetric Encryption - ví dụ thuật toán AES) có đặc điểm căn bản nào?",
                "options": [
                    "A. Sử dụng cùng một khóa duy nhất cho cả hai quá trình mã hóa và giải mã dữ liệu.",
                    "B. Sử dụng hai khóa hoàn toàn khác nhau cho mã hóa và giải mã.",
                    "C. Không thể giải mã được sau khi đã mã hóa.",
                    "D. Chỉ chạy được trên các máy tính lượng tử."
                ],
                "answer": 0,
                "trap": "Đối xứng = Dùng CHUNG 1 CHÌA KHÓA (như ổ khóa nhà bình thường). Bất đối xứng = Dùng CẶP 2 CHÌA KHÓA khác nhau (Public và Private).",
                "explanation": "Mã hóa đối xứng sử dụng một khóa bí mật duy nhất để mã hóa văn bản gốc thành bản mã và giải mã ngược lại. Ưu điểm là tốc độ tính toán cực nhanh, phù hợp mã hóa khối dữ liệu lớn."
            },
            {
                "id": 19,
                "question": "Hành vi nào sau đây là vi phạm quy định tại Luật An ninh mạng của Việt Nam?",
                "options": [
                    "A. Lập trình một trang web học tập và chia sẻ kiến thức miễn phí cho học sinh.",
                    "B. Soạn thảo, đăng tải, tán phát thông tin bịa đặt, sai sự thật gây hoang mang trong nhân dân hoặc xúc phạm danh dự, nhân phẩm của tổ chức, cá nhân trên không gian mạng.",
                    "C. Sử dụng mật khẩu có độ dài 16 ký tự để bảo vệ tài khoản cá nhân.",
                    "D. Cài đặt phần mềm diệt virus bản quyền trên máy tính cá nhân."
                ],
                "answer": 1,
                "trap": "Học sinh thường nghĩ mạng xã hội là 'ảo' nên muốn đăng gì cũng được. Luật An ninh mạng nghiêm cấm hành vi bịa đặt tin giả, xúc phạm danh dự người khác và có chế tài xử phạt hành chính hoặc hình sự rất nghiêm khắc.",
                "explanation": "Theo Điều 8 Luật An ninh mạng 2018, nghiêm cấm việc đưa thông tin sai sự thật, vu khống, xúc phạm uy tín tổ chức hoặc danh dự, nhân phẩm của cá nhân trên không gian mạng."
            },
            {
                "id": 20,
                "question": "Khi máy tính bất ngờ có các dấu hiệu: quạt tản nhiệt quay rú rít hết công suất, máy đơ giật dù không mở ứng dụng nào nặng, lưu lượng mạng tải lên tăng đột biến, nguyên nhân khả nghi nhất là:",
                "options": [
                    "A. Máy tính đang tự động dọn dẹp vệ sinh bụi bẩn bên trong thùng máy.",
                    "B. Máy tính có thể đã bị nhiễm mã độc đào tiền ảo ngầm (Cryptojacking) hoặc đang bị biến thành máy tính ma (Zombie) tham gia mạng lưới tấn công DDoS.",
                    "C. Màn hình máy tính đang được sưởi ấm.",
                    "D. Cáp chuột quang bị cắm ngược đầu."
                ],
                "answer": 1,
                "trap": "Nhiều người nghĩ máy đơ do Windows nặng, nhưng quạt rú liên tục và mạng tải lên 100% là triệu chứng điển hình của mã độc đào coin ngầm chiếm đoạt CPU/GPU của nạn nhân.",
                "explanation": "Mã độc đào tiền mã hóa (Cryptomining malware/Cryptojacking) bí mật vắt kiệt tài nguyên xử lý CPU/GPU của máy tính nạn nhân để đào tiền cho kẻ tấn công, gây nóng máy, hao điện và giảm thọ phần cứng."
            }
        ]
    }
}


def get_quiz_for_topic(topic_id: str):
    """Lấy danh sách 20 câu hỏi trắc nghiệm kèm bẫy & giải thích cho chuyên đề THPT."""
    return THPT_QUIZZES.get(str(topic_id))


def get_all_quiz_summaries():
    """Lấy danh sách tóm tắt các chuyên đề trắc nghiệm."""
    summaries = []
    for tid, data in THPT_QUIZZES.items():
        summaries.append({
            "topic_id": tid,
            "topic_title": data["topic_title"],
            "description": data["description"],
            "total_questions": len(data["questions"])
        })
    return summaries
