// Simple Activity Tracker - Pure localStorage, no database
class ActivityTracker {
  constructor() {
    this.storageKey = 'smartFileOrganizerActivity';
    this.maxActivities = 15;
  }

  getActivities() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      const activities = stored ? JSON.parse(stored) : [];
      
      // Update relative times for existing activities
      const updatedActivities = activities.map(activity => ({
        ...activity,
        time: this.getRelativeTime(new Date(activity.timestamp))
      }));
      
      return updatedActivities;
    } catch (error) {
      console.error('Error loading activities:', error);
      return [];
    }
  }

  addActivity(action, details = {}) {
    try {
      const activities = this.getActivities();
      const newActivity = {
        id: Date.now() + Math.random(), // Ensure uniqueness
        action,
        time: 'Just now',
        timestamp: new Date().toISOString(),
        type: this.getActivityType(action),
        details
      };

      activities.unshift(newActivity);
      
      // Keep only recent activities
      const recentActivities = activities.slice(0, this.maxActivities);
      
      localStorage.setItem(this.storageKey, JSON.stringify(recentActivities));
      return this.getActivities(); // Return with updated times
    } catch (error) {
      console.error('Error adding activity:', error);
      return this.getActivities();
    }
  }

  getActivityType(action) {
    const actionLower = action.toLowerCase();
    if (actionLower.includes('organized') || actionLower.includes('files')) return 'healthcare';
    if (actionLower.includes('indexed') || actionLower.includes('search')) return 'index';
    if (actionLower.includes('screenshot')) return 'screenshots';
    if (actionLower.includes('folder') || actionLower.includes('opened')) return 'settings';
    if (actionLower.includes('statistics') || actionLower.includes('viewed')) return 'stats';
    return 'general';
  }

  getRelativeTime(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    return date.toLocaleDateString();
  }

  clearActivities() {
    try {
      localStorage.removeItem(this.storageKey);
      return [];
    } catch (error) {
      console.error('Error clearing activities:', error);
      return [];
    }
  }
}

export default ActivityTracker;