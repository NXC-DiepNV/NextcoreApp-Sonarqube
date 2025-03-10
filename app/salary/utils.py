from utils.mail_core import MailCore


class Utils:

    @staticmethod
    def calculate_tax(income: float) -> float:
        if income < 5000000:
            return income * 0.05
        elif income < 10000000:
            return income * 0.10 - 250000
        elif income < 18000000:
            return income * 0.15 - 750000
        elif income < 32000000:
            return income * 0.20 - 1650000
        elif income < 52000000:
            return income * 0.25 - 3250000
        elif income < 80000000:
            return income * 0.30 - 5850000
        else:
            return income * 0.35 - 9850000
        
    @staticmethod
    def send_payslips(mail_client: MailCore, payslips: dict, payslip_file: str):

        mail_client.send_email(
            
            to_email=payslips["email_member"],
            subject=f'Phiếu lương {payslips["date_pay_period"]}',
            body=f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <p>Thân gửi bạn {payslips["full_name"]},</p>
                <p>Chúng tôi xin gửi đến bạn phiếu lương của kỳ lương tháng <strong>{payslips["date_pay_period"]}</strong>. Vui lòng xem chi tiết trong tệp đính kèm.</p>
                <p><strong>Lưu ý:</strong> Mật khẩu để mở phiếu lương là <strong>sinh nhật của bạn (DDMMYYYY)</strong>.</p>
                <p>Trân trọng,</p>
                <p>Nextcore Software JSC</p>
                <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
                <p style="font-size: 0.9em; color: #555;">Email này được gửi tự động. Vui lòng không trả lời trực tiếp email này.</p>
            </body>
            </html>
            """,
            attachment=payslip_file,
            type='html'
        )    
