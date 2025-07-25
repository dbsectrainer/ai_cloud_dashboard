import streamlit as st
import pandas as pd


def display_learning_resources():
    """Display learning resources and certification paths."""
    st.title("🎓 Learning Resources")

    # US Cloud & AI Platforms
    st.subheader("US Cloud & AI Platforms")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **AWS Learning Path**
        - [AWS Certified Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/)
        - [AWS Solutions Architect](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
        - [AWS Machine Learning Specialty](https://aws.amazon.com/certification/certified-machine-learning-specialty/)
        
        **Azure Learning Path**
        - [Azure Fundamentals (AZ-900)](https://learn.microsoft.com/en-us/certifications/azure-fundamentals/)
        - [Azure Solutions Architect](https://learn.microsoft.com/en-us/certifications/azure-solutions-architect/)
        - [Azure AI Engineer](https://learn.microsoft.com/en-us/certifications/azure-ai-engineer/)
        """
        )

    with col2:
        st.markdown(
            """
        **Google Cloud Path**
        - [Cloud Digital Leader](https://cloud.google.com/certification/cloud-digital-leader)
        - [Professional Cloud Architect](https://cloud.google.com/certification/cloud-architect)
        - [Professional Machine Learning Engineer](https://cloud.google.com/certification/machine-learning-engineer)
        
        **Free Resources**
        - [AWS Skill Builder](https://explore.skillbuilder.aws/)
        - [Microsoft Learn](https://learn.microsoft.com/)
        - [Google Cloud Training](https://cloud.google.com/training)
        """
        )

    # Chinese Platforms
    st.subheader("Chinese Cloud & AI Platforms")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **Alibaba Cloud**
        - [Alibaba Cloud Certification](https://edu.alibabacloud.com/certification)
        - [Cloud Computing Certification](https://edu.alibabacloud.com/certification/ace)
        - [Machine Learning Certification](https://edu.alibabacloud.com/certification/machine-learning)
        
        **Tencent Cloud**
        - [Cloud Practitioner](https://cloud.tencent.com/edu/training/cert/introduction)
        - [Solutions Architect](https://cloud.tencent.com/edu/training/cert/introduction)
        - [Cloud Developer](https://cloud.tencent.com/edu/training/cert/introduction)
        """
        )

    with col2:
        st.markdown(
            """
        **Baidu AI**
        - [Baidu AI Certification](https://ai.baidu.com/certification)
        - [PaddlePaddle Framework](https://www.paddlepaddle.org.cn/documentation/docs/en/guides/index_en.html)
        
        **Free Resources**
        - [Alibaba Cloud Academy](https://edu.alibabacloud.com/)
        - [Tencent Cloud EDU](https://cloud.tencent.com/edu)
        - [Baidu AI Studio](https://aistudio.baidu.com/aistudio/index)
        """
        )

    # European Platforms
    st.subheader("European Cloud & AI Platforms")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **OVHcloud**
        - [OVHcloud Academy](https://academy.ovhcloud.com/)
        - [Infrastructure Certifications](https://academy.ovhcloud.com/certification/)
        - [Cloud Solutions](https://academy.ovhcloud.com/certification/)
        
        **Scaleway**
        - [Scaleway Training](https://www.scaleway.com/en/docs/)
        - [Infrastructure Basics](https://www.scaleway.com/en/docs/tutorials/)
        """
        )

    with col2:
        st.markdown(
            """
        **European AI**
        - [Mistral AI Documentation](https://docs.mistral.ai/)
        - [Aleph Alpha Academy](https://www.aleph-alpha.com/academy)
        
        **Free Resources**
        - [OVHcloud Tutorials](https://docs.ovh.com/gb/en/tutorials/)
        - [Scaleway Documentation](https://www.scaleway.com/en/docs/)
        """
        )

    # Additional Resources
    st.subheader("Additional Learning Resources")

    st.markdown(
        """
    **Multi-Cloud Learning**
    - [A Cloud Guru](https://acloudguru.com/) - Comprehensive cloud training
    - [Cloud Academy](https://cloudacademy.com/) - Multi-platform learning paths
    - [Coursera Cloud Specializations](https://www.coursera.org/browse/information-technology/cloud-computing)
    - [edX Cloud Computing Courses](https://www.edx.org/learn/cloud-computing)
    
    **AI & Machine Learning**
    - [Fast.ai](https://www.fast.ai/) - Practical Deep Learning
    - [Hugging Face Courses](https://huggingface.co/learn) - NLP and Transformers
    - [DeepLearning.AI](https://www.deeplearning.ai/) - AI Specializations
    - [MLOps Learning Path](https://ml-ops.org/content/mlops-learning-path)
    
    **Security & Compliance**
    - [Cloud Security Alliance](https://cloudsecurityalliance.org/education/)
    - [GDPR Certification](https://gdpr.eu/certification/)
    - [ISO 27001 Training](https://www.iso.org/isoiec-27001-information-security.html)
    """
    )

    # Comparison Tools
    st.subheader("Certification Comparison")

    cert_data = pd.DataFrame(
        {
            "Certification Level": [
                "Entry Level",
                "Associate",
                "Professional",
                "Specialty",
            ],
            "Time Investment": ["1-2 months", "2-4 months", "4-6 months", "3-6 months"],
            "Typical Cost": ["$100-150", "$150-300", "$300-500", "$300-400"],
            "Career Impact": [
                "Foundation knowledge",
                "Junior positions",
                "Senior positions",
                "Expert roles",
            ],
        }
    )

    st.dataframe(cert_data, use_container_width=True)
