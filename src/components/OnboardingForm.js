


import React, { useState } from "react";
import { Form, Input, Select, Button, Typography } from "antd";
import "../styles/onboarding.css";
import { useLang } from "../components/LangContext"; // 👈 Import the custom hook
import WhatsAppChatWidget from "./WhatsAppChatWidget"; // Import the WhatsApp widget
import Climate from "./Climate"

const { Title } = Typography;
const { Option } = Select;

const OnboardingForm = () => {
  const { t } = useLang(); // 👈 Access the global translation function
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  // Define arrays using translation keys
  const orgTypesMap = {
    "org_type_fpo": t("org_type_fpo"),
    "org_type_pacs": t("org_type_pacs"),
    "org_type_finance": t("org_type_finance"),
    "org_type_agritech": t("org_type_agritech"),
    "org_type_input_supplier": t("org_type_input_supplier"),
    "org_type_market_buyer": t("org_type_market_buyer"),
    "org_type_sustainability": t("org_type_sustainability"),
    "org_type_other": t("org_type_other"),
  };

  const partnershipReasonsMap = {
    "reason_marketplace": t("reason_marketplace"),
    "reason_financial_services": t("reason_financial_services"),
    "reason_supply_chain": t("reason_supply_chain"),
    "reason_sustainability": t("reason_sustainability"),
    "reason_digital_transformation": t("reason_digital_transformation"),
    "reason_other": t("reason_other"),
  };

  // Convert maps to array format for rendering
  const orgTypes = Object.values(orgTypesMap);
  const partnershipReasons = Object.values(partnershipReasonsMap);


  const onFinish = async (values) => {
    setLoading(true);
    try {
      const response = await fetch("https://admin.agrifabrix.in/api/static/Onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      const data = await response.json();

      if (response.ok) {
        // Use translated success message
        alert(data.message || t("onboarding_alert_success"));
        form.resetFields();
      } else {
        // Use translated failure message
        alert(data.error || t("onboarding_alert_failed_generic"));
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      // Use translated error message
      alert(t("onboarding_alert_failed_generic"));
    } finally {
      setLoading(false);
    }
  };

  const onFinishFailed = () => {
    // Use translated validation alert
    alert(t("onboarding_alert_failed_validation"));
  };

  return (
    <div className="form-wrapper">
      <div className="form-heading-container">
        <Title level={3}>{t("onboarding_title")}</Title>
      </div>

      <div className="onboarding-form-container">
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          {/* Contact Person Name */}
          <Form.Item
            label={t("onboarding_label_name")}
            name="contactName"
            rules={[
              { required: true, message: t("onboarding_required_name") },
            ]}
            className="small-input"
          >
            <Input />
          </Form.Item>

          {/* Phone Number */}
          <Form.Item
            label={t("onboarding_label_phone")}
            name="phone"
            rules={[
              { required: true, message: t("onboarding_required_phone") },
            ]}
            className="small-input"
          >
            <Input type="tel" />
          </Form.Item>

          {/* Email */}
          <Form.Item
            label={t("onboarding_label_email")}
            name="email"
            rules={[
              { required: true, message: t("onboarding_required_email"), type: "email" },
            ]}
            className="small-input"
          >
            <Input />
          </Form.Item>

          {/* Type of Organization */}
          <Form.Item
            label={t("onboarding_label_org_type")}
            name="orgType"
            rules={[
              { required: true, message: t("onboarding_required_select_type") },
            ]}
          >
            <Select
              mode="multiple"
              placeholder={t("onboarding_placeholder_org_type")}
            >
              {orgTypes.map((type) => (
                <Option key={type} value={type}>
                  {type}
                </Option>
              ))}
            </Select>
          </Form.Item>

          {/* Primary Reason for Partnering */}
          <Form.Item
            label={t("onboarding_label_reason")}
            name="partnershipReason"
            rules={[
              { required: true, message: t("onboarding_required_select_reason") },
            ]}
          >
            <Select
              mode="multiple"
              placeholder={t("onboarding_placeholder_reason")}
            >
              {partnershipReasons.map((reason) => (
                <Option key={reason} value={reason}>
                  {reason}
                </Option>
              ))}
            </Select>
          </Form.Item>

          {/* Submit Button */}
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              disabled={loading}
            >
              {/* Translated button text */}
              {loading ? t("onboarding_button_submitting") : t("onboarding_button_submit")}
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default OnboardingForm;