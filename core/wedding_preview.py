from django.shortcuts import render, get_object_or_404
from .models import WeddingEvent
from django.http import HttpResponseRedirect
from django.conf import settings

def wedding_event_preview(request, wedding_slug):
    """
    Preview page for wedding events - shows event details and redirects to local wedding page
    Similar to event_detail_page but for WeddingEvent model
    """
    wedding = get_object_or_404(WeddingEvent, slug=wedding_slug)
    
    # Check if request is from a bot/crawler (for social sharing)
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_bot = any(bot in user_agent for bot in [
        'googlebot', 'facebookexternalhit', 'twitterbot', 'linkedinbot',
        'whatsapp', 'telegram', 'slackbot', 'applebot', 'bingbot'
    ])
    
    if is_bot:
        # Render HTML preview for bots/social media
        context = {
            'wedding': wedding,
            'title': wedding.event_title,
            'description': f"{wedding.bride_name} & {wedding.groom_name}'s Wedding",
            'image': wedding.bride_image.url if wedding.bride_image else None,
            'url': f"http://savemeaseatzambia.com/api/wedding-events/{wedding.slug}/preview/",
        }
        return render(request, 'wedding_event_preview.html', context)
    else:
        # Redirect to savemeaseat Zambia website with dynamic slug
        redirect_url = f"https://savemeaseatzambia.com/wedding2.html?slug={wedding.slug}/"
        return HttpResponseRedirect(redirect_url)
